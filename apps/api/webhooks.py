# coding: utf-8
# 📂 apps/api/webhooks.py - معالج الويب هوك السيادي (النسخة النهائية)

import hmac
import hashlib
import logging
from flask import Blueprint, request, jsonify
from config import Config 
from apps.extensions import db
from apps.models.orders_db import ProcessedOrder

# إعداد المسار والسجلات
webhooks_bp = Blueprint('webhooks', __name__)
logger = logging.getLogger(__name__)

@webhooks_bp.route('/webhooks', methods=['POST'])
def handle_qumra_webhook():
    """
    نقطة النهاية لاستقبال أحداث الويب هوك من منصة قمرا.
    """
    
    # 1. الحصول على التوقيع من الترويسات (Headers)
    # ملاحظة: قم بتجربة التوقيع المرسل من قمرا في السجلات
    signature = request.headers.get('X-WebHook-Signature') or request.headers.get('X-Signature')
    
    if not signature:
        logger.warning("⚠️ محاولة وصول بدون توقيع!")
        return jsonify({"error": "Missing signature"}), 401

    # 2. التحقق من التوقيع الأمني
    # نستخدم .strip() لإزالة أي مسافات زائدة قد تكون حدثت عند نسخ المفتاح إلى Render
    secret = Config.WEBHOOK_SECRET.strip().encode('utf-8')
    payload = request.get_data() 
    
    expected_signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()

    # سجلات للمقارنة (تظهر في Render Logs - هذا هو مفتاح الحل للـ 403)
    logger.info(f"Expected Sig: {expected_signature}")
    logger.info(f"Received Sig: {signature}")

    # المقارنة الآمنة ضد هجمات التوقيت
    if not hmac.compare_digest(expected_signature, signature):
        logger.error("🚫 محاولة وصول بتوقيع غير صالح!")
        return jsonify({"error": "Invalid signature"}), 403

    # 3. استخراج ومعالجة بيانات الويب هوك
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
        
    # سجل كاشف للبيانات - سيظهر في Logs لترى هيكل الطلب القادم من قمرا
    logger.info(f"DEBUG: Data Received: {data}")
    
    event = data.get('event')
    order_data = data.get('data', {})

    logger.info(f"✅ تم استلام ويب هوك نوع: {event}")

    # 4. معالجة وحفظ الطلب في قاعدة البيانات
    if event in ['order/created', 'order/updated', 'cart/created']:
        # نحاول الحصول على معرف الطلب، قد يكون id أو _id بناءً على هيكل الويب هوك
        order_id = str(order_data.get('id') or order_data.get('_id', ''))
        
        if order_id:
            order = ProcessedOrder.query.get(order_id)
            if not order:
                order = ProcessedOrder(id=order_id)
            
            order.status = order_data.get('status', 'pending')
            
            # محاولة استخراج القيمة المالية بأمان
            total_data = order_data.get('total', {})
            total_amount = total_data.get('amount', 0.0) if isinstance(total_data, dict) else 0.0
            order.total_price = float(total_amount)
            
            try:
                db.session.add(order)
                db.session.commit()
                logger.info(f"💾 تم حفظ الطلب {order_id} بنجاح.")
            except Exception as e:
                db.session.rollback()
                logger.error(f"❌ خطأ أثناء حفظ الطلب {order_id}: {e}")
                return jsonify({"error": "Database error"}), 500

    return jsonify({"status": "success"}), 200

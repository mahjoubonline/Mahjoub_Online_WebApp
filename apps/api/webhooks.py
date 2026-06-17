# coding: utf-8
# 📂 apps/api/webhooks.py - معالج الويب هوك السيادي مع أدوات التشخيص

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
    # 1. تشخيص الترويسات (للتعرف على اسم التوقيع الصحيح الذي ترسل به قمرا)
    logger.info(f"Incoming Request Headers: {dict(request.headers)}")
    
    # نحاول جلب التوقيع من الاسم الشائع (يمكنك تغييره بناءً على ما ستراه في السجلات)
    signature = request.headers.get('X-WebHook-Signature') or request.headers.get('X-Signature')
    
    if not signature:
        logger.warning("⚠️ محاولة وصول بدون توقيع!")
        return jsonify({"error": "Missing signature"}), 401

    # 2. التحقق من التوقيع الأمني
    secret = Config.WEBHOOK_SECRET.encode('utf-8')
    payload = request.data # استخدام البيانات الخام للتطابق مع تشفير قمرا
    expected_signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()

    # سجلات للمقارنة (تظهر في Render Logs)
    logger.info(f"Expected: {expected_signature}")
    logger.info(f"Received: {signature}")

    if not hmac.compare_digest(expected_signature, signature):
        logger.error("🚫 محاولة وصول بتوقيع غير صالح!")
        return jsonify({"error": "Invalid signature"}), 403

    # 3. استخراج ومعالجة بيانات الويب هوك
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
        
    event = data.get('event')
    order_data = data.get('data', {})

    logger.info(f"✅ تم استلام ويب هوك نوع: {event}")

    # 4. معالجة وحفظ الطلب
    if event in ['order/created', 'order/updated', 'cart/created']:
        order_id = str(order_data.get('id', ''))
        
        if order_id:
            order = ProcessedOrder.query.get(order_id)
            if not order:
                order = ProcessedOrder(id=order_id)
            
            order.status = order_data.get('status', 'pending')
            
            # تحديث القيمة المالية المشفرة تلقائياً
            total_amount = order_data.get('total', {}).get('amount', 0.0)
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

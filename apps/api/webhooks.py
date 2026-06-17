from flask import Blueprint, request, jsonify
import hmac
import hashlib
import logging
import os
from apps import Config

# إعداد السجلات لمراقبة الطلبات في Render Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

webhooks_bp = Blueprint('webhooks', __name__)

# استخدام مفتاح التوقيع من الإعدادات التي أضفناها سابقاً
WEBHOOK_SECRET = Config.WEBHOOK_SECRET

def verify_signature(data, signature):
    """التحقق من أن الطلب قادم فعلاً من منصة قمرا"""
    if not WEBHOOK_SECRET:
        return True # إذا لم يوجد مفتاح أمان، نقبل الطلب (للتطوير فقط)
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        data,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)

@webhooks_bp.route('/api/webhooks/qumra', methods=['POST'])
def handle_qumra_webhook():
    # 1. التحقق من التوقيع الأمني
    signature = request.headers.get('X-WebHook-Signature')
    if not signature or not verify_signature(request.data, signature):
        logger.error("Invalid Webhook Signature!")
        return jsonify({"error": "Invalid signature"}), 403

    # 2. استقبال البيانات
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    logger.info(f"✅ Webhook Received: {data.get('event', 'unknown event')}")
    
    # 3. هنا تبدأ منطق معالجة الأحداث
    # مثال: إذا كان الطلب 'order/created' نقوم بتشغيل دالة معينة
    event_type = data.get('event')
    
    if event_type == 'cart/created':
        # أضف هنا كود التعامل مع إنشاء السلة
        logger.info(f"Processing Cart: {data.get('data', {}).get('_id')}")
    
    # الرد على المنصة بأننا استلمنا البيانات بنجاح
    return jsonify({"status": "success"}), 200

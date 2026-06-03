# coding: utf-8
# 📂 apps/utils/whatsapp/webhook_handler.py - محرك استقبال إشارات واتساب

from flask import request, jsonify
import logging

# إعداد السجلات لمتابعة الرسائل (Log)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_whatsapp_webhook():
    """
    دالة استقبال إشارات الواتساب (Webhook).
    تقوم بالتحقق من صحة الاتصال ومعالجة الرسائل الواردة.
    """
    
    # 1. التحقق من التحدي (Verification Challenge) الذي يرسله واتساب
    if request.args.get("hub.mode") == "subscribe":
        hub_verify_token = request.args.get("hub.verify_token")
        # قارن هذا الـ TOKEN بالذي ستضعه في إعدادات Facebook Developer
        if hub_verify_token == "YOUR_VERIFY_TOKEN":
            return request.args.get("hub.challenge"), 200
        return "Verification token mismatch", 403

    # 2. استقبال بيانات الرسالة
    data = request.get_json()
    logger.info(f"Received webhook: {data}")

    if data and 'entry' in data:
        for entry in data['entry']:
            for change in entry.get('changes', []):
                value = change.get('value', {})
                if 'messages' in value:
                    # هنا يتم معالجة الرسالة الواردة
                    process_message(value['messages'][0])

    return jsonify({"status": "received"}), 200

def process_message(message):
    """منطق معالجة محتوى الرسالة الواردة"""
    sender = message.get('from')
    text = message.get('text', {}).get('body')
    
    logger.info(f"Message from {sender}: {text}")
    # هنا ستضيف المنطق: إذا كان المستخدم يطلب OTP، نقوم بتوليده وإرساله

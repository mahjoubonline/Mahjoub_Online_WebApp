# coding: utf-8
# 📂 api/webhook.py - محرك استقبال وإرسال رسائل واتساب

import requests
from flask import Blueprint, request, current_app

# إنشاء Blueprint لتنظيم الـ API
webhook_bp = Blueprint('webhook_bp', __name__)

def send_whatsapp_message(to_phone, message_body):
    """دالة لإرسال رد عبر واتساب باستخدام الإعدادات المركزية"""
    phone_id = current_app.config.get('WHATSAPP_PHONE_NUMBER_ID')
    token = current_app.config.get('WHATSAPP_ACCESS_TOKEN')
    
    if not phone_id or not token:
        print("❌ Error: WhatsApp configuration missing.")
        return None

    url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "text": {"body": message_body}
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

@webhook_bp.route('/webhook', methods=['GET', 'POST'])
def handle_webhook():
    # 1. التحقق من التوصيل (Verification)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == current_app.config.get('WHATSAPP_VERIFY_TOKEN'):
            return challenge, 200
        return 'Forbidden', 403

    # 2. استقبال الرسائل (Payload Processing)
    elif request.method == 'POST':
        data = request.get_json()
        
        try:
            # التحقق من وجود رسالة نصية في هيكل البيانات
            if 'messages' in data['entry'][0]['changes'][0]['value']:
                message_info = data['entry'][0]['changes'][0]['value']['messages'][0]
                sender_phone = message_info['from']
                message_text = message_info['text']['body']
                
                print(f"📥 Received message from {sender_phone}: {message_text}")
                
                # يمكنك هنا إضافة منطق الـ OTP أو الردود الذكية
                reply_message = "أهلاً بك يا هندسة في محجوب أونلاين! لقد استلمت رسالتك بنجاح."
                send_whatsapp_message(sender_phone, reply_message)
        
        except (KeyError, IndexError):
            # تجاهل أي أحداث أخرى لا تهمنا (مثل تحديثات الحالة)
            pass

        return 'OK', 200

import os
import requests
from config import Config

def send_whatsapp_otp(phone, otp_code):
    """الربط الفعلي مع WhatsApp Business API مع معالجة أخطاء أفضل"""
    
    # محاولة جلب التوكن من الـ Config أو من متغيرات البيئة مباشرة كحل احتياطي
    token = getattr(Config, 'WHATSAPP_ACCESS_TOKEN', None) or os.environ.get('WHATSAPP_ACCESS_TOKEN')
    phone_id = getattr(Config, 'WHATSAPP_PHONE_NUMBER_ID', None) or os.environ.get('WHATSAPP_PHONE_NUMBER_ID')

    # طباعة للتصحيح (ستظهر في Logs في Render)
    print(f"DEBUG: Attempting to send OTP to {phone}")
    print(f"DEBUG: Token exists: {token is not None}, PhoneID exists: {phone_id is not None}")

    if not token or not phone_id:
        print("ERROR: Missing WhatsApp Configuration in environment variables!")
        return False

    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": "otp_verification_template", 
            "language": {"code": "ar"},
            "components": [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": str(otp_code)}]
                }
            ]
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"ERROR: Facebook API responded with {response.status_code}: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: Connection to Facebook failed: {str(e)}")
        return False

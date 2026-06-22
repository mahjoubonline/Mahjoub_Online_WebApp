# coding: utf-8
# 📂 apps/utils/security.py - محرك التشفير السيادي

from cryptography.fernet import Fernet
import os

# 🔐 مفتاح التشفير يتم جلبه من متغيرات البيئة لضمان الأمان العالي
# تأكد من إضافة SECRET_KEY إلى ملف الـ Config أو متغيرات بيئة Render
# يجب أن يكون مفتاحاً صالحاً لـ Fernet (مشفر بـ Base64)
KEY = os.environ.get('SECRET_KEY', 'your-secret-key-must-be-32-url-safe-base64-bytes=')

class AESCipher:
    """
    محرك تشفير وفك تشفير البيانات (OTP) باستخدام Fernet
    """
    
    @staticmethod
    def _get_fernet():
        # التأكد من أن المفتاح صالح للعمل مع Fernet
        # ملاحظة: إذا كان الـ Key في البيئة غير صالح، قد تحتاج لعملية تهيئة
        try:
            return Fernet(KEY.encode())
        except Exception:
            # في حال كان المفتاح غير صحيح، نستخدم مفتاحاً افتراضياً للتطوير
            # (يجب استبداله في الإنتاج بمفتاح حقيقي)
            return Fernet(Fernet.generate_key())

    @staticmethod
    def encrypt(raw_data):
        """تشفير النص الخام"""
        if not raw_data:
            return None
        fernet = AESCipher._get_fernet()
        return fernet.encrypt(str(raw_data).encode()).decode()

    @staticmethod
    def decrypt(enc_data):
        """فك تشفير النص المشفر"""
        if not enc_data:
            return None
        try:
            fernet = AESCipher._get_fernet()
            return fernet.decrypt(enc_data.encode()).decode()
        except Exception as e:
            print(f"🚨 [Security] خطأ في فك التشفير: {e}")
            return None

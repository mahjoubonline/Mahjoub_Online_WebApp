# coding: utf-8
# 📂 apps/utils/security.py - محرك التشفير السيادي (مُحدث لدعم الاستيراد من جذر المشروع)

import os
import sys
from cryptography.fernet import Fernet

# إضافة مسار جذر المشروع إلى النظام لضمان العثور على config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from config import Config
except ImportError:
    # احتياط: في حال فشل الاستيراد، نستخدم مفتاحاً افتراضياً لمنع انهيار النظام
    class Config:
        ENCRYPTION_KEY = 'your-fallback-key-must-be-32-base64-bytes=='

class AESCipher:
    """محرك التشفير المعتمد على المفتاح المركزي في Config"""
    
    @staticmethod
    def _get_fernet():
        # استخدام المفتاح الموجود في ملف config.py
        # تأكد أن المفتاح المذكور في config.py هو Base64 صالح لـ Fernet
        key = Config.ENCRYPTION_KEY.encode()
        return Fernet(key)

    @staticmethod
    def encrypt(raw_data):
        if not raw_data: return None
        return AESCipher._get_fernet().encrypt(str(raw_data).encode()).decode()

    @staticmethod
    def decrypt(enc_data):
        if not enc_data: return None
        try:
            return AESCipher._get_fernet().decrypt(enc_data.encode()).decode()
        except Exception:
            # إذا فشل الفك (مفتاح خاطئ أو بيانات تالفة)، نرجع None
            return None

# 📂 apps/utils/security.py
from cryptography.fernet import Fernet
import os

class AESCipher:
    def __init__(self, key):
        # تأكد من وجود المفتاح في متغيرات البيئة
        self.cipher = Fernet(key)
    
    def encrypt(self, raw):
        return self.cipher.encrypt(raw.encode()).decode()
    
    def decrypt(self, enc):
        return self.cipher.decrypt(enc.encode()).decode()

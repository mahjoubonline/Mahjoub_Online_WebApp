from apps import db
from datetime import datetime
from cryptography.fernet import Fernet
import os

def get_cipher_suite():
    """الحصول على المفتاح من البيئة وتهيئته بشكل صحيح"""
    key = os.environ.get('ENCRYPTION_KEY')
    
    if key:
        # تأكد من أن المفتاح هو string بنفس تنسيق Fernet.generate_key()
        # لا نستخدم .encode('utf-8') على النص الخام، بل نستخدم المفتاح كما هو
        try:
            return Fernet(key.encode('utf-8'))
        except Exception as e:
            print(f"❌ Error initializing Fernet: {e}")
            raise ValueError("ENCRYPTION_KEY غير صالح. يجب أن يكون 32-byte url-safe base64.")
    
    # في حال عدم وجود مفتاح، نولد مفتاحاً تجريبياً (للتطوير فقط)
    new_key = Fernet.generate_key()
    print(f"⚠️ WARNING: No ENCRYPTION_KEY found. Please add this to your ENV: {new_key.decode('utf-8')}")
    return Fernet(new_key)

# تهيئة التشفير
cipher_suite = get_cipher_suite()

def encrypt(value):
    if value is None: return None
    return cipher_suite.encrypt(str(value).encode('utf-8')).decode('utf-8')

def decrypt(value):
    if value is None: return None
    try:
        return cipher_suite.decrypt(value.encode('utf-8')).decode('utf-8')
    except Exception:
        return "0.0"

# ... باقي الكود كما هو (كلاسات Product و ProductVariant)

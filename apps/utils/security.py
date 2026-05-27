# coding: utf-8
from cryptography.fernet import Fernet
import os

class AESCipher:
    def __init__(self, key=None):
        """
        تهيئة أداة التشفير باستخدام مفتاح من المتغيرات البيئية.
        """
        # جلب المفتاح من المتغير البيئي ENCRYPTION_KEY
        self.raw_key = key or os.getenv('ENCRYPTION_KEY')
        
        if not self.raw_key:
            # في حال عدم وجود مفتاح، ننشئ مفتاحاً عشوائياً (للتطوير فقط)
            print("⚠️ تحذير: ENCRYPTION_KEY غير موجود! يتم إنشاء مفتاح مؤقت.")
            self.key = Fernet.generate_key()
        else:
            self.key = self.raw_key.encode()

        try:
            self.cipher = Fernet(self.key)
        except Exception as e:
            print(f"❌ خطأ في تهيئة Fernet: {e}")
            # في حال كان المفتاح غير صالح (مثلاً ليس Base64)، ننشئ مفتاحاً جديداً
            self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)

    def encrypt(self, plain_text):
        """تشفير النص."""
        if not plain_text:
            return None
        return self.cipher.encrypt(str(plain_text).encode()).decode()

    def decrypt(self, cipher_text):
        """فك تشفير النص."""
        if not cipher_text:
            return None
        return self.cipher.decrypt(str(cipher_text).encode()).decode()

    def decrypt_to_float(self, value):
        """
        دالة ذكية لمعالجة البيانات:
        تحاول فك التشفير أولاً، وإذا فشلت أو لم تكن مشفرة، تحول القيمة لرقم.
        """
        if value is None:
            return 0.0
        
        str_val = str(value).strip()
        
        # إذا كانت القيمة تبدأ بـ gAAAAA فهي مشفرة بـ Fernet
        if str_val.startswith('gAAAAA'):
            try:
                decrypted = self.decrypt(str_val)
                return float(decrypted)
            except Exception:
                # في حال فشل فك التشفير لأي سبب (مفتاح خطأ مثلاً)
                return 0.0
        
        # إذا كانت ليست مشفرة، حاول تحويلها مباشرة
        try:
            return float(str_val)
        except ValueError:
            return 0.0

# كائن جاهز للاستخدام في جميع أنحاء التطبيق
cipher_suite = AESCipher()

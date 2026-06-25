# 📂 apps/models/otp_db.py

class OTPVerification(db.Model):
    # ... (ابقِ كل شيء كما هو) ...

    @staticmethod
    def generate_otp(identifier, dispatcher, expires_in_minutes=5):
        # تم تعطيل النظام لصالح الدخول بكلمة المرور
        return None

    @staticmethod
    def verify_otp(identifier, input_code):
        # تم تعطيل النظام لصالح الدخول بكلمة المرور
        return False

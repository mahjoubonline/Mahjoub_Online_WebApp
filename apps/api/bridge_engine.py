# 📂 apps/api/bridge_engine.py
# محرك الإرسال السيادي - Bridge Engine
# الإصدار: مستقر (Singleton)

import logging
from whatsapp_web_python import WhatsApp

# إعداد سجلات الخطأ لمراقبة المحرك
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BridgeEngine:
    def __init__(self, session_name="sovereign_session"):
        try:
            self.bot = WhatsApp(session=session_name)
            logger.info("✅ [Bridge] تم تهيئة المحرك السيادي بنجاح.")
        except Exception as e:
            logger.error(f"❌ [Bridge] فشل في تهيئة المحرك: {e}")
            self.bot = None

    def dispatch(self, phone, message):
        """إرسال الرسالة مباشرة عبر الواتساب المرتبط"""
        if not self.bot:
            return False, "المحرك غير مهيأ (Bot not initialized)"
            
        try:
            # تنظيف الرقم (مثال: +967 779... -> 967779...)
            clean_phone = str(phone).replace("+", "").replace(" ", "").replace("-", "")
            
            # تنفيذ الإرسال
            self.bot.send_message(clean_phone, message)
            logger.info(f"🚀 [Bridge] تم الإرسال إلى {clean_phone}")
            return True, "تم الإرسال بنجاح"
            
        except Exception as e:
            logger.error(f"⚠️ [Bridge] خطأ أثناء الإرسال: {e}")
            return False, str(e)

# تهيئة المحرك ليتم استخدامه في كامل التطبيق كـ Singleton
engine = BridgeEngine()

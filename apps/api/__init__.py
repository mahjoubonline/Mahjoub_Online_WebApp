# 📂 apps/api/__init__.py

# استيراد الـ Blueprint الخاص بالـ Webhooks لسهولة التسجيل في تطبيق Flask الرئيسي
from .webhooks import webhooks_bp

# استيراد محرك المزامنة/الإرسال السيادي ليكون متاحاً للاستخدام المباشر
from .sync_engine import SyncEngine

# إنشاء نسخة من المحرك ليتم استخدامها في كامل التطبيق (Singleton)
engine = SyncEngine()

# تعريف ما يتم تصديره عند استدعاء الحزمة
__all__ = ['webhooks_bp', 'engine']

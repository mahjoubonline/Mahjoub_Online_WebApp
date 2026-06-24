# 📂 apps/suppliers_auth_portal/__init__.py
from apps.suppliers_auth_portal.routes import suppliers_bp

# يمكنك إضافة أي تهيئة خاصة للموديول هنا إذا لزم الأمر لاحقاً، 
# مثل إعدادات الأمان الخاصة أو متغيرات البيئة.
__all__ = ['suppliers_bp']

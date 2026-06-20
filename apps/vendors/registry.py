# coding: utf-8
# 📂 apps/vendors/registry.py - سجل الهوية والربط الذاتي لنظام الموردين

from .routes import vendors_bp

# مصفوفة المكونات المسجلة تلقائياً للتصدير الخارجي
__all__ = ['VENDOR_MODULE']

# كائن التسجيل التلقائي الموحد للمنصة
VENDOR_MODULE = {
    'name': 'vendors',
    'blueprint': vendors_bp,
    'prefix': '/vendors',
    'enabled': True,
    'icon': 'bi-shop',          # الأيقونة الرسمية في لوحة تحكم الإدارة العليا
    'title': 'نظام حوكمة الموردين'
}

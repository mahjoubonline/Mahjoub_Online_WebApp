import os
from core.extensions import db

def initialize_sovereign_system(app):
    """محرك التأسيس التلقائي: يبني المجلدات والجداول ويطهر الكاش"""
    
    # 1. قائمة المجلدات المطلوبة للهيكل النمطي الجديد
    required_dirs = [
        'core/models',
        'apps/supplier_app/templates',
        'apps/finance_app/templates',
        'apps/governance_app/templates',
        'static/css',
        'static/js'
    ]

    print("🛡️ بدء بروتوكول التأسيس السيادي...")

    # 2. إنشاء المجلدات إذا كانت مفقودة
    for folder in required_dirs:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ تم إنشاء المجلد: {folder}")

    # 3. بناء قاعدة البيانات داخل سياق التطبيق
    with app.app_context():
        try:
            # استيراد الموديلات هنا ليعرفها SQLAlchemy
            from core.models.supplier_db import Supplier
            # سيتم إضافة الموديلات الأخرى هنا (audit_db, finance_db)
            
            db.create_all()
            print("💎 تم بناء الهيكل الجدولي في قاعدة البيانات بنجاح.")
        except Exception as e:
            print(f"⚠️ تنبيه أثناء بناء الجداول: {e}")

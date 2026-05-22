from flask import Blueprint, render_template, request, redirect, url_for, flash
from apps import db 
# التعديل الحاسم: استيراد كلاس المورد مباشرة من الملف الفعلي للنماذج لقاعدة البيانات
from apps.models.admin_db import Supplier  

# تعريف الـ Blueprint الخاص بلوحة التحكم المركزية
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

@admin_dashboard.route('/dashboard')
# @login_required  # قم بتفعيلها لحماية لوحة التحكم لاحقاً عند اكتمال جلسات التحقق
def dashboard():
    try:
        # جلب كافة شركاء النجاح (الموردين) من قاعدة بيانات Postgres بترتيب الأحدث أولاً
        suppliers = Supplier.query.order_by(Supplier.id.desc()).all()
        suppliers_count = len(suppliers)
    except Exception as e:
        # تأمين مرن: مصفوفة فارغة لمنع انهيار الخادم 500 في حال عدم وجود الجدول أو التهيئة
        suppliers = []
        suppliers_count = 0

    # تمرير البيانات الحية إلى قالب العرض الكامل والمحدث بالهوية البنفسجية الملكية
    return render_template(
        'admin/dashboard_content.html', 
        suppliers=suppliers, 
        suppliers_count=suppliers_count
    )

@admin_dashboard.route('/settings')
# @login_required
def system_settings():
    # مسار خاص بإعدادات السيادة
    return render_template('admin/admin_base.html')

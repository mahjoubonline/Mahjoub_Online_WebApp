from flask import Blueprint, render_template, request, redirect, url_for, flash
# استيراد نموذج الموردين وقاعدة البيانات (قم بتعديل المسار والمسميات حسب ملف الـ models لديك)
from apps import db 
from apps.models import Supplier  # تأكد من مطابقة اسم النموذج ومكانه لديك

# تعريف الـ Blueprint الخاص بلوحة التحكم المركزية
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

@admin_dashboard.route('/dashboard')
# @login_required  # قم بتفعيلها إذا كنت تستخدم flask_login لحماية لوحة التحكم
def dashboard():
    try:
        # جلب كافة الموردين المعتمدين من قاعدة البيانات بترتيب تنازلي (الأحدث أولاً)
        suppliers = Supplier.query.order_by(Supplier.id.desc()).all()
        suppliers_count = len(suppliers)
    except Exception as e:
        # في حال لم تكن قاعدة البيانات أو الجدول جاهزاً بعد، نضع مصفوفة فارغة لتجنب انهيار الصفحة
        suppliers = []
        suppliers_count = 0
        # flash(f"تنبيه أثناء الاتصال بقاعدة البيانات: {str(e)}", "warning")

    # تمرير البيانات الفورية إلى قالب العرض الكامل المحدث
    return render_template(
        'admin/dashboard_content.html', 
        suppliers=suppliers, 
        suppliers_count=suppliers_count
    )

@admin_dashboard.route('/settings')
# @login_required
def system_settings():
    # مسار إعدادات السيادة (يمكنك ربطه بقالب مخصص لاحقاً)
    return render_template('admin/admin_base.html') # أو اسم قالب الإعدادات المخصص

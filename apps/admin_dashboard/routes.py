# coding: utf-8
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier
# يمكنك إضافة استيراد موديلات أخرى هنا عند الحاجة

# تعريف الـ Blueprint الخاص بلوحة التحكم
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/admin/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    """
    مركز القيادة السيادي: يعرض ملخص العمليات والحالة العامة للنظام
    """
    # جلب البيانات من قاعدة البيانات (استعلامات مستقلة)
    total_suppliers = Supplier.query.count()
    
    # إعداد كائن البيانات الذي يتوقعه القالب (dashboard_content.html)
    stats = {
        'total_suppliers': total_suppliers,
        'active_orders': 0,        # يمكن تطويرها لترتبط بجدول الطلبات
        'system_health': '100% مستقر',
        'server_status': 'Online'
    }
    
    # تمرير البيانات للقالب
    return render_template('admin/dashboard_content.html', 
                           current_user=current_user, 
                           stats=stats)

@admin_dashboard.route('/admin/settings', methods=['GET'])
@login_required
def system_settings():
    """
    مسار إعدادات السيادة
    """
    return render_template('admin/settings.html')

# يرجى التأكد من إضافة هذا المسار في ملف routes.py الخاص بالموردين 
# أو إبقاؤه هنا إذا كنت تفضل إدارة قائمة الموردين من الداشبورد
@admin_dashboard.route('/admin/suppliers/list', methods=['GET'])
@login_required
def list_suppliers():
    suppliers = Supplier.query.all()
    return render_template('admin/suppliers.html', suppliers=suppliers)

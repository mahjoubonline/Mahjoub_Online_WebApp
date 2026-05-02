from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user
from . import admin_bp
from .auth import handle_admin_login
# من المفترض استيراد الموديلات هنا لاحقاً (مثل User, Supplier, Order, WithdrawRequest)

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """معالجة تسجيل دخول السلطة العليا"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """مركز المراقبة والتحكم المركزي"""
    # هذه البيانات يتم تمريرها للقالب dashboard.html
    stats = {
        'orders_count': "1,250", 
        'suppliers_count': "48",
        'total_balance': "15,500",
        'pending_requests': "12",
        'active_users': "320"
    }
    # تم التعديل لاستدعاء dashboard.html الموجود في مجلد templates الخاص بـ admin_panel
    return render_template('dashboard.html', **stats)

# --- قسم حوكمة الموردين ---

@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_vendor():
    """تعميد مورد جديد في النظام الملكي"""
    if request.method == 'POST':
        # منطق حفظ البيانات وتوليد الرقم السيادي سيضاف هنا
        # "النجاح يبنى بالثقة وليس على الأوراق"
        flash('تم تعميد المورد بنجاح وفتح محافظه المالية الثلاث.', 'success')
        return redirect(url_for('admin.manage_suppliers'))
    
    return render_template('add_supplier.html')

@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    """حوكمة الموردين المعتمدين"""
    return render_template('manage_suppliers.html')

# --- قسم الهندسة المالية ---

@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    """إدارة طلبات سحب الأرصدة والتسويات"""
    return render_template('withdraw_requests.html')

@admin_bp.route('/financial-engineering')
@login_required
def financial_reports():
    """تقارير الهندسة المالية والأرباح"""
    return render_template('financial_reports.html')

# --- إعدادات السيادة ---

@admin_bp.route('/system-settings')
@login_required
def system_settings():
    """إعدادات السيادة والتحكم بالنظام"""
    return render_template('settings.html')

@admin_bp.route('/logout')
@login_required
def logout():
    """إنهاء الجلسة الآمنة والعودة للشرنقة"""
    logout_user()
    flash('تم إنهاء الجلسة الآمنة بنجاح. ننتظر عودتك يا قائد.', 'info')
    return redirect(url_for('admin.admin_login'))

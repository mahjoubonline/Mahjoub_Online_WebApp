# admin_panel/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user
from . import admin_bp

# 🛡️ استدعاء الخدمات (المنطق البرمجي معزول تماماً)
from core.services.supplier_service import get_all_suppliers, get_next_supplier_id
from core.services.stats_service import get_admin_dashboard_stats
from .auth import login_view 

# ==========================================
# 1. نظام الدخول والخروج (Access Control)
# ==========================================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ استدعاء واجهة الدخول - تأكد من وجود مفتاح CSRF في القالب """
    return login_view()

@admin_bp.route('/logout')
@login_required
def logout():
    """ إنهاء الجلسة والعودة لنقطة الصفر """
    logout_user()
    flash("تم إنهاء الجلسة السيادية بنجاح.", "info")
    return redirect(url_for('admin.login'))

# ==========================================
# 2. لوحة القيادة والرادارات (Views)
# ==========================================

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """ استدعاء رادار الإحصائيات الشامل """
    stats = get_admin_dashboard_stats()
    return render_template('admin/dashboard.html', **stats)

@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    """ استدعاء سجل الموردين المعتمدين """
    try:
        data = get_all_suppliers()
        return render_template('admin/manage_suppliers.html', **data)
    except Exception as e:
        flash(f"عطل في استدعاء بيانات الموردين: {str(e)}", "danger")
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/suppliers/add', methods=['GET'])
@login_required
def add_supplier():
    """ استدعاء نموذج تعميد مورد جديد """
    next_id = get_next_supplier_id()
    return render_template('admin/add_supplier.html', next_id=next_id)

# ==========================================
# توثيق الربط البرمجي (للقائد علي محجوب):
# 1. تم توجيه القوالب لمجلد 'admin/' لضمان عدم التداخل مع مجلد 'staff/'.
# 2. هذا الملف يعمل كـ "بوابة" فقط، معالجة البيانات (Logic) تتم في ملفات الـ services.
# 3. روابط الـ Staff يتم استدعاؤها عبر Blueprint منفصل (staff_bp) مسجل في app.py.
# ==========================================

# admin_panel/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, logout_user
from core import db
from core.models.user import User
from core.models.supplier import Supplier
from datetime import datetime

# استيراد البلوبرنت
from . import admin_bp
from .auth import login_view 

# ==========================================
# 1. بوابة الولوج (The Login Gate)
# ==========================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """تفعيل بوابة الدخول السيادية - نقطة الصفر للنظام"""
    return login_view()

# ==========================================
# 2. غرفة القيادة (Dashboard)
# ==========================================
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """عرض الرادار العام وإحصائيات الترسانة الرقمية"""
    try:
        # إحصائيات سريعة من المحرك المالي والقاعدة
        data = {
            'users_count': User.query.count(),
            'suppliers_count': Supplier.query.count(),
            'orders_count': 0, 
            'total_yer': db.session.query(db.func.sum(Supplier.balance_yer)).scalar() or 0.0,
            'total_sar': db.session.query(db.func.sum(Supplier.balance_sar)).scalar() or 0.0,
            'total_usd': db.session.query(db.func.sum(Supplier.balance_usd)).scalar() or 0.0,
            'now': datetime.now()
        }
        return render_template('admin/dashboard.html', **data)
    except Exception as e:
        print(f"⚠️ خطأ في رادار القيادة: {e}")
        return "حدث خطأ في جلب البيانات المالية، تأكد من استقرار قاعدة البيانات."

# ==========================================
# 3. إدارة العرض (Management Views)
# ==========================================
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    """عرض قائمة الموردين المؤرشفين"""
    suppliers = Supplier.query.order_by(Supplier.created_at.desc()).all()
    return render_template('admin/manage_suppliers.html', suppliers=suppliers)

# ==========================================
# 4. بروتوكول الخروج الآمن (Logout)
# ==========================================
@admin_bp.route('/logout')
@login_required
def logout():
    """تأمين الخروج والعودة لبوابة الولوج الخارجية"""
    logout_user()
    flash("تم تسجيل الخروج من مركز القيادة بنجاح. النظام الآن في وضع الحماية.", "info")
    return redirect(url_for('admin.login'))

# ==========================================
# 5. تأمين المسارات (Security Middleware)
# ==========================================
@admin_bp.before_request
def check_maintenance():
    """بروتوكول فحص الصيانة قبل كل طلب"""
    pass

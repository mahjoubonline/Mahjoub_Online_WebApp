# admin_panel/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, logout_user
from core import db
from core.models.user import User
from core.models.supplier import Supplier
from datetime import datetime
import traceback

# 1. استيراد البلوبرنت
from . import admin_bp
from .auth import login_view 

# ==========================================
# 1. بوابة الولوج (The Login Gate)
# ==========================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    return login_view()

# ==========================================
# 2. غرفة القيادة (Dashboard)
# ==========================================
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """عرض إحصائيات النظام الأساسية مع نظام حماية مركزية"""
    try:
        # حساب الإحصائيات مع قيم افتراضية آمنة
        data = {
            'users_count': User.query.count() or 0,
            'suppliers_count': Supplier.query.count() or 0,
            'orders_count': 0, 
            
            # حساب السيولة مع معالجة القيم الفارغة
            'total_yer': db.session.query(db.func.sum(Supplier.balance_yer)).scalar() or 0.0,
            'total_sar': db.session.query(db.func.sum(Supplier.balance_sar)).scalar() or 0.0,
            'total_usd': db.session.query(db.func.sum(Supplier.balance_usd)).scalar() or 0.0,
            
            'now': datetime.now()
        }
        # تأكد من أن المسار هو admin/dashboard.html
        return render_template('admin/dashboard.html', **data)
        
    except Exception as e:
        # نظام رصد الأخطاء المتقدم - سيظهر لك السطر المسبب للمشكلة بالضبط
        error_details = traceback.format_exc()
        return f"""
        <div dir="rtl" style="font-family: sans-serif; padding: 20px; color: #721c24; background: #f8d7da; border: 1px solid #f5c6cb;">
            <h3>⚠️ خلل في رادار القيادة المركزية</h3>
            <p>يوجد تعارض في قوالب العرض أو قاعدة البيانات. تفاصيل العطل:</p>
            <pre style="text-align: left; background: #fff; padding: 15px;">{error_details}</pre>
            <hr>
            <a href="{url_for('admin.logout')}">الرجوع لتسجيل الدخول</a>
        </div>
        """

# ==========================================
# 3. إدارة الموردين (Suppliers)
# ==========================================
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    """عرض الموردين مع تعطيل الفلاتر المسببة للانهيار"""
    try:
        suppliers = Supplier.query.order_by(Supplier.id.desc()).limit(20).all()
        
        # تم تصفير 'sovereign' لأن عمود 'tier' غير موجود في قاعدة البيانات حالياً (كما في الصورة)
        stats = {
            'total': Supplier.query.count() or 0,
            'active': Supplier.query.filter_by(status='active').count() or 0,
            'sovereign': 0 
        }
        
        return render_template('admin/manage_suppliers.html', 
                               suppliers=suppliers, 
                               stats=stats)
    except Exception as e:
        return f"⚠️ خطأ في إدارة الموردين: {e}"

# ==========================================
# 4. بروتوكول الخروج الآمن (Logout)
# ==========================================
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج. النظام في وضع الحماية.", "info")
    return redirect(url_for('admin.login'))

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
    """عرض إحصائيات النظام الأساسية مع حماية ضد الانهيار"""
    try:
        # حساب الإحصائيات مع التأكد من وجود قيم افتراضية (0) في حال كانت القاعدة فارغة
        users_count = User.query.count() or 0
        suppliers_count = Supplier.query.count() or 0
        
        # رصد السيولة باستخدام استعلامات آمنة
        total_yer = db.session.query(db.func.sum(Supplier.balance_yer)).scalar() or 0.0
        total_sar = db.session.query(db.func.sum(Supplier.balance_sar)).scalar() or 0.0
        total_usd = db.session.query(db.func.sum(Supplier.balance_usd)).scalar() or 0.0
        
        data = {
            'users_count': users_count,
            'suppliers_count': suppliers_count,
            'orders_count': 0, # سيتم الربط مع API قمرة مستقبلاً
            'total_yer': total_yer,
            'total_sar': total_sar,
            'total_usd': total_usd,
            'now': datetime.now()
        }
        
        return render_template('admin/dashboard.html', **data)
        
    except Exception as e:
        # في حال حدوث خطأ، سيتم إظهار تفاصيل الخطأ بدلاً من صفحة بيضاء
        # هذا يساعدك في معرفة إذا كان هناك نقص في أعمدة قاعدة البيانات
        error_info = traceback.format_exc()
        return f"""
        <div dir="rtl" style="font-family: 'Cairo', sans-serif; padding: 20px; border: 2px solid red;">
            <h2 style="color

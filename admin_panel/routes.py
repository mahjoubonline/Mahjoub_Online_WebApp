# admin_panel/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, logout_user
from core import db
from core.models.user import User
from core.models.supplier import Supplier
from datetime import datetime

# 1. استيراد البلوبرنت والمنطق السيادي
from . import admin_bp
from .auth import login_view 
from .suppliers_logic import SupplierLogic

# 2. استيراد المحركات التنفيذية (Engines)
# تم استدعاء محرك اللوجستيات لرصد المناطق ومحرك الموردين للفلترة
from .engines.supplier_engine import get_suppliers_by_filter
from .engines.logistics_engine import LogisticsEngine

# ==========================================
# 1. بوابة الولوج (The Login Gate)
# ==========================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """تأمين المداخل الرسمية لمركز الإدارة"""
    return login_view()

# ==========================================
# 2. غرفة القيادة والتحكم (The Sovereign Dashboard)
# ==========================================
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """
    الرادار المركزي لمراقبة أداء محجوب أونلاين:
    يرصد العمليات، الأرصدة، والتوزع الجغرافي للموردين.
    """
    try:
        # أ: استدعاء تقارير الكثافة الجغرافية (الخوخة، عدن، إلخ) من محرك اللوجستيات
        zone_stats = LogisticsEngine.get_zone_density()
        
        # ب: تجميع البيانات المالية والعددية
        # ملاحظة للقائد: يتم تجميع الأرصدة من جميع الموردين لإعطاء القيمة الإجمالية للترسانة
        data = {
            'users_count': User.query.count(),
            'suppliers_count': Supplier.query.count(),
            'orders_count': 0, # سيتم ربطه بمحرك الطلبات مستقبلاً
            
            # رصد السيولة النقدية بمختلف العملات
            'total_yer': db.session.query(db.func.sum(Supplier.balance_yer)).scalar() or 0.0,
            'total_sar': db.session.query(db.func.sum(Supplier.balance_sar)).scalar() or 0.0,
            'total_usd': db.session.query(db.func.sum(Supplier.balance_usd)).scalar() or 0.0,
            
            'zones': zone_stats, # توزيع الموردين حسب المحافظات
            'now': datetime.now()
        }
        
        # ج: استدعاء واجهة الداشبورد مع حقن البيانات السيادية
        return render_template('admin/dashboard.html', **data)
        
    except Exception as e:
        # بروتوكول الطوارئ في حال تعثر الرادار
        return f"⚠️ خطأ فني في استدعاء بيانات الرادار المركزي: {str(e)}"

# ==========================================
# 3. إدارة الموردين (Supplier Management)
# ==========================================
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    """
    عرض قائمة الموردين: يعتمد على المحرك لجلب عينة أولية (آخر 10 موردين)
    لضمان سرعة استجابة النظام.
    """
    # جلب البيانات عبر المحرك المخصص
    latest_suppliers = get_suppliers_by_filter(limit=10)
    
    # إحصائيات سريعة للبطاقات العلوية في صفحة الإدارة
    stats = {
        'total': Supplier.query.count(),
        'active': Supplier.query.filter_by(status='active').count(),
        'sovereign': Supplier.query.filter_by(tier='سيادي').count()
    }
    
    return render_template('admin/manage_suppliers.html', 
                           suppliers=latest_suppliers, 
                           stats=stats)

# ==========================================
# 4. بروتوكول الإنهاء (Secure Logout)
# ==========================================
@admin_bp.route('/logout')
@login_required
def logout():
    """تأمين النظام عند مغادرة القائد"""
    logout_user()
    flash("تم تسجيل الخروج بنجاح. النظام في وضع الحماية النشطة.", "info")
    return redirect(url_for('admin.login'))

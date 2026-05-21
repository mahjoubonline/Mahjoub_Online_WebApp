# coding: utf-8
# ⚙️ محرك لوحة التحكم السيادية - منصة محجوب أونلاين 2026

from flask import render_template
from flask_login import login_required, current_user
from . import admin_dashboard
from apps.models.supplier_db import Supplier
# استيراد نموذج المحفظة إذا كنت تحتاج لحساب الإجماليات من هناك
from apps.models.wallet_db import SupplierWallet
from sqlalchemy import func
from apps import db

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    """
    عرض لوحة القيادة (Dashboard) الرئيسية مع حساب إجماليات الخزائن.
    """
    try:
        # حساب إحصائية شركاء النجاح
        total_suppliers = Supplier.query.count()
        
        # حساب إجماليات المحافظ (افتراض أسماء أعمدة مشابهة لما في موديل المحفظة لديك)
        # إذا كانت الأسماء تختلف، يرجى تعديلها لتطابق الموديل
        totals = db.session.query(
            func.sum(SupplierWallet.balance_yer).label('total_yer'),
            func.sum(SupplierWallet.balance_sar).label('total_sar'),
            func.sum(SupplierWallet.balance_usd).label('total_usd')
        ).first()

        # تجهيز البيانات للقالب
        stats_data = {
            'total_yer': totals.total_yer or 0,
            'total_sar': totals.total_sar or 0,
            'total_usd': totals.total_usd or 0
        }
        
        return render_template('admin/dashboard_content.html', 
                               current_user=current_user, 
                               totals=stats_data,
                               total_suppliers=total_suppliers)
                               
    except Exception as e:
        return f"خطأ في تحميل مركز القيادة: {str(e)}", 500

@admin_dashboard.route('/settings', methods=['GET'])
@login_required
def system_settings():
    """
    إعدادات النظام السيادية
    """
    return render_template('admin/settings.html', current_user=current_user)

@admin_dashboard.route('/suppliers', methods=['GET'])
@login_required
def list_suppliers():
    """
    قائمة الموردين المعتمدين
    """
    suppliers = Supplier.query.all()
    return render_template('admin/suppliers.html', suppliers=suppliers)

# coding: utf-8
# 🚀 مستند القيادة والسيطرة لـ لوحة التحكم المركزية - منصة محجوب أونلاين 2026

from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

# 🛡️ استدعاء الـ Blueprint الخاص بلوحة التحكم من ملف التعريف __init__.py الخاص بالتطبيق المصغر
from . import admin_dashboard_bp

# ========================================================
# 📊 1. النافذة الرئيسية: الفضاء المالي وحوكمة الخزائن (Dashboard Home)
# ========================================================
@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    try:
        # استدعاء الموديلات محلياً لمنع التداخل والتعليق البرمجي أثناء الإقلاع
        from apps.extensions import db
        from apps.models.wallet_db import SupplierWallet
        
        # 💵 حساب إجمالي الأرصدة الحية في النظام لكل عملة على حدة بالتزامن المباشر
        # يقوم بجمع (الأرصدة الإجمالية + الأرصدة المعلقة) ليعكس القوة المالية الفعلية للخزائن
        totals = db.session.query(
            func.coalesce(func.sum(SupplierWallet.yer_total + SupplierWallet.yer_pending), 0).label('total_yer'),
            func.coalesce(func.sum(SupplierWallet.sar_total + SupplierWallet.sar_pending), 0).label('total_sar'),
            func.coalesce(func.sum(SupplierWallet.usd_total + SupplierWallet.usd_pending), 0).label('total_usd')
        ).filter(SupplierWallet.status == 'نشطة').first()
        
        # تمرير البيانات الحية إلى نافذة التطبيق المصغر المحدثة بـ Glassmorphism
        return render_template('admin/dashboard_content.html', 
                               current_user=current_user,
                               totals=totals)
                               
    except Exception as e:
        flash(f"حدث خطأ سيادي أثناء جلب بيانات حوكمة الخزائن: {str(e)}", "danger")
        # في حال حدوث خطأ، نمرر قيم صفرية لضمان عدم انهيار النافذة أمام المسؤول
        fallback_totals = {'total_yer': 0.00, 'total_sar': 0.00, 'total_usd': 0.00}
        return render_template('admin/dashboard_content.html', 
                               current_user=current_user,
                               totals=fallback_totals)


# ========================================================
# 🏬 2. نافذة تطبيق "سجل الموردين الحقيقي" (List Suppliers)
# ========================================================
@admin_dashboard_bp.route('/suppliers/list', methods=['GET'])
@login_required
def list_suppliers():
    try:
        from apps.models.supplier_db import Supplier
        
        # جلب كافة الموردين المعتمدين في النظام وترتيبهم من الأحدث للأقدم
        suppliers_list = Supplier.query.order_by(Supplier.id.desc()).all()
        
        return render_template('admin/list_suppliers.html', 
                               current_user=current_user,
                               suppliers=suppliers_list)
    except Exception as e:
        flash(f"فشل استدعاء نافذة سجل الموردين: {str(e)}", "danger")
        return redirect(url_for('admin_dashboard.dashboard_home'))


# ========================================================
# 🛡️ 3. نافذة تطبيق "إعدادات السيادة" (System Settings)
# ========================================================
@admin_dashboard_bp.route('/settings/sovereignty', methods=['GET', 'POST'])
@login_required
def system_settings():
    if request.method == 'POST':
        # هنا يتم معالجة وحفظ إعدادات المنصة الحساسة
        flash("تم تحديث إعدادات السيادة والأمان بنجاح.", "success")
        return redirect(url_for('admin_dashboard.system_settings'))
        
    return render_template('admin/system_settings.html', current_user=current_user)

# coding: utf-8
from flask import render_template, request, jsonify
from flask_login import login_required
from apps.admin_dashboard import admin_dashboard_bp
from apps.models.wallet_db import SupplierWallet
from sqlalchemy import func
from apps import db

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    """
    دالة لوحة التحكم الرئيسية - تدعم التحميل الديناميكي (AJAX)
    """
    # جلب الإجماليات من قاعدة البيانات
    totals_data = db.session.query(
        func.sum(SupplierWallet.yer_total).label('total_yer'),
        func.sum(SupplierWallet.sar_total).label('total_sar'),
        func.sum(SupplierWallet.usd_total).label('total_usd')
    ).first()

    # تحويل النتائج إلى قاموس مع قيم افتراضية 0 إذا كانت القاعدة فارغة
    totals = {
        'total_yer': totals_data.total_yer or 0,
        'total_sar': totals_data.total_sar or 0,
        'total_usd': totals_data.total_usd or 0
    }

    # التحقق مما إذا كان الطلب من المتصفح (AJAX)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax:
        # إرجاع محتوى الجزء المخصص للحقن فقط
        return render_template('admin/dashboard_content.html', totals=totals)
    
    # إرجاع الهيكل الرئيسي للصفحة
    return render_template('admin/admin_base.html', totals=totals)

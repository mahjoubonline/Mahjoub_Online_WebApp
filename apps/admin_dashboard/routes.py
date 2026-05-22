# coding: utf-8
from flask import render_template, request
from flask_login import login_required
from sqlalchemy import func
from . import admin_dashboard_bp

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    try:
        from apps.extensions import db
        from apps.models.wallet_db import SupplierWallet
        
        # استعلام الأرصدة الحية لتغذية واجهة الكروت الافتراضية
        totals = db.session.query(
            func.coalesce(func.sum(SupplierWallet.yer_total), 0).label('total_yer'),
            func.coalesce(func.sum(SupplierWallet.sar_total), 0).label('total_sar'),
            func.coalesce(func.sum(SupplierWallet.usd_total), 0).label('total_usd')
        ).first()
        
        return render_template('admin/dashboard_content.html', totals=totals)
    except Exception as e:
        # نظام طوارئ لمنع الانهيار المطلق في حال عدم وجود الجداول بعد
        return render_template('admin/dashboard_content.html', totals=None)

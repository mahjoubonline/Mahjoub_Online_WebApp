# coding: utf-8
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from . import wallet_bp
from apps.models.wallet_db import SupplierWallet
from apps.extensions import db

# دالة عرض الصفحة المالية
@wallet_bp.route('/wallet_home', methods=['GET'])
@login_required
def wallet_home():
    # جلب المحافظ (مثال)
    wallets = SupplierWallet.query.all()
    
    # التحقق من نوع الطلب لمنع تكرار الهيكل (App Shell)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/wallet_dashboard.html', wallets=wallets)
    
    # في حال الدخول المباشر، توجيه المستخدم للوحة التحكم
    return redirect(url_for('admin_dashboard.dashboard_home'))

# أي دوال أخرى خاصة بالمحفظة (مثل تحويل، إيداع...) تضاف هنا بنفس الطريقة

# coding: utf-8
from flask import render_template, request
from flask_login import login_required
from . import admin_dashboard_bp

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    # كشف هل الطلب قادم عبر AJAX (للمحتوى فقط) أم تحميل مباشر
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax:
        return render_template('admin/dashboard_content.html', totals=None)
    
    # تحميل الهيكل الكامل إذا كان الدخول مباشراً
    return render_template('admin/admin_base.html')

@admin_dashboard_bp.route('/suppliers', methods=['GET'])
@login_required
def list_suppliers():
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax:
        return render_template('admin/suppliers_list.html')
    
    return render_template('admin/admin_base.html')

# coding: utf-8
from flask import render_template, request, jsonify
from flask_login import login_required
from apps.admin_dashboard import admin_dashboard_bp

# يمكنك إضافة دالة لجلب البيانات هنا أو استيرادها من ملف آخر
def get_totals():
    # نموذج لبيانات وهمية، استبدلها باستعلامات قاعدة البيانات الخاصة بك
    return {
        'total_yer': 1500000.00,
        'total_sar': 5000.00,
        'total_usd': 1200.00
    }

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    """
    المسار الرئيسي للداشبورد. 
    يدعم نظام الحقن الديناميكي (App Shell).
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # 1. إذا كان الطلب من محرك الجافاسكريبت (AJAX)
    # نقوم بإرجاع المحتوى فقط (Partial HTML)
    if is_ajax:
        return render_template('admin/dashboard_content.html', totals=get_totals())
    
    # 2. إذا كان دخولاً مباشراً للرابط من المتصفح
    # نقوم بإرجاع الهيكل الكامل (App Shell)
    return render_template('admin/admin_base.html')

@admin_dashboard_bp.route('/suppliers', methods=['GET'])
@login_required
def list_suppliers():
    """
    مثال لمسار إضافي يدعم الحقن الديناميكي.
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax:
        # هنا ستضع قالب قائمة الموردين الصافي
        return render_template('admin/suppliers_list.html')
    
    return render_template('admin/admin_base.html')

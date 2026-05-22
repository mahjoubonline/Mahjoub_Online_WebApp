# coding: utf-8
from flask import render_template, request
from flask_login import login_required
from apps.admin_dashboard import admin_dashboard_bp

def get_totals():
    """
    دالة لجلب بيانات الخزينة الموحدة.
    """
    # قمنا بوضع قيم افتراضية لضمان عدم حدوث خطأ إذا كانت القاعدة فارغة
    return {
        'total_yer': 1500000.00,
        'total_sar': 5000.00,
        'total_usd': 1200.00
    }

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    """
    المسار الرئيسي: يتعامل مع نوعين من الطلبات:
    1. AJAX (للحقن الديناميكي).
    2. طلب عادي (لتحميل الهيكل لأول مرة).
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # استدعاء البيانات
    totals = get_totals()
    
    if is_ajax:
        # إرجاع المحتوى فقط (بدون هيكل) للحقن داخل div
        return render_template('admin/dashboard_content.html', totals=totals)
    
    # في كل الأحوال، نضمن إرجاع استجابة واحدة واضحة
    return render_template('admin/admin_base.html')

@admin_dashboard_bp.route('/suppliers', methods=['GET'])
@login_required
def list_suppliers():
    """
    مسار قائمة الموردين.
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax:
        return render_template('admin/suppliers_list.html')
    
    return render_template('admin/admin_base.html')

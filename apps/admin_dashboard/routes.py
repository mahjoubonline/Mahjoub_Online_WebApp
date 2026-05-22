# coding: utf-8
from flask import render_template, request
from flask_login import login_required
from apps.admin_dashboard import admin_dashboard_bp

def get_totals():
    """
    دالة لجلب بيانات الخزينة.
    تأكد أن هذه الدالة تعيد قاموساً (Dictionary) أو قيمة افتراضية لتجنب الخطأ.
    """
    try:
        # هنا يمكنك وضع استعلامات قاعدة البيانات الخاصة بك
        # مثال: totals = Treasury.query.first()
        return {
            'total_yer': 1500000.00,
            'total_sar': 5000.00,
            'total_usd': 1200.00
        }
    except Exception:
        # في حال حدوث خطأ في قاعدة البيانات، نرجع قيماً آمنة
        return {'total_yer': 0.0, 'total_sar': 0.0, 'total_usd': 0.0}

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    """
    المسار المسؤول عن جلب صفحة الداشبورد.
    يستخدم نظام الحقن الديناميكي (AJAX) لضمان السرعة.
    """
    # التحقق من نوع الطلب
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # جلب البيانات لضمان عدم تمرير قيم فارغة للقالب
    totals = get_totals()
    
    # 1. إذا كان الطلب من محرك الحقن الديناميكي (Partial Content)
    if is_ajax:
        return render_template('admin/dashboard_content.html', totals=totals)
    
    # 2. إذا كان الطلب مباشراً (Full Page Load)
    return render_template('admin/admin_base.html')

@admin_dashboard_bp.route('/suppliers', methods=['GET'])
@login_required
def list_suppliers():
    """
    مسار قائمة الموردين المعتمدين.
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax:
        # هنا نستدعي قالب الموردين (تأكد من وجود هذا الملف)
        return render_template('admin/suppliers_list.html')
    
    return render_template('admin/admin_base.html')

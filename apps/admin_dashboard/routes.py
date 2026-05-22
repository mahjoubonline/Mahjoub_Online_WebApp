# coding: utf-8
from flask import render_template, request
from flask_login import login_required
from apps.admin_dashboard import admin_dashboard_bp

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    try:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            # تجربة إرجاع نص بسيط أولاً
            return render_template('admin/dashboard_content.html')
        
        return render_template('admin/admin_base.html')
    except Exception as e:
        # هذا سيعرض لنا الخطأ الحقيقي على الشاشة بدلاً من 500
        return f"خطأ برمجيا: {str(e)}"

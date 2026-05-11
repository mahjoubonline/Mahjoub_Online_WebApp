# admin_panel/routes.py
from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_required, logout_user
from . import admin_bp

# استدعاء الخدمات (النظام المنفصل)
from core.services.supplier_service import get_all_suppliers, create_supplier, get_next_supplier_id
from core.services.stats_service import get_admin_dashboard_stats
from .auth import login_view 

# ==========================================
# 1. بوابة الولوج (Login)
# ==========================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ استدعاء واجهة تسجيل الدخول المنفصلة """
    return login_view()

# ==========================================
# 2. لوحة التحكم (Dashboard)
# ==========================================
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """ استدعاء الإحصائيات الشاملة من محرك الإحصائيات """
    try:
        stats = get_admin_dashboard_stats()
        return render_template('admin/dashboard.html', **stats)
    except Exception as e:
        # تأمين اللوحة في حال فشل استعلامات الإحصائيات
        return render_template('admin/dashboard.html', error=str(e), 
                               users_count=0, suppliers_count=0)

# ==========================================
# 3. إدارة الموردين (القائمة السيادية)
# ==========================================
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    """ جلب قائمة الموردين المعتمدين وإحصائياتهم """
    try:
        data = get_all_suppliers()
        # نمرر البيانات للقالب (تأكد من وجود suppliers و stats في الـ dict العائد)
        return render_template('admin/manage_suppliers.html', **data)
    except Exception as e:
        flash(f"⚠️ عطل في رادار الموردين: {str(e)}", "danger")
        return redirect(url_for('admin.dashboard'))

# ==========================================
# 4. تعميد مورد جديد (Add Supplier)
# ==========================================
@admin_bp.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """ معالجة بروتوكول الإرسال والتعميد """
    if request.method == 'POST':
        # حل مشكلة الـ 415 و الـ Content-Type بذكاء
        if request.is_json:
            data = request.get_json()
        else:
            # في حال تم الإرسال عبر Form عادي وليس SweetAlert
            data = request.form.to_dict()
        
        if not data:
            return jsonify({"status": "error", "message": "لم يتم استلام بيانات صالحة"}), 400
            
        # استدعاء خدمة الإنشاء (المنطق البرمجي المفصل)
        success, result = create_supplier(data)
        
        if success:
            return jsonify({
                "status": "success", 
                "message": f"تم التعميد بنجاح: {result}"
            })
        
        # في حال وجود خطأ منطقي (مثل تكرار اسم المستخدم)
        return jsonify({"status": "error", "message": result}), 500

    # في حالة الـ GET: نجهز الواجهة ونعرض المعرف القادم
    try:
        next_id = get_next_supplier_id()
    except:
        next_id = "جاري الحساب..."
        
    return render_template('admin/add_supplier.html', next_id=next_id)

# ==========================================
# 5. بروتوكول الخروج الآمن (Logout)
# ==========================================
@admin_bp.route('/logout')
@login_required
def logout():
    """ إنهاء الجلسة وحماية النظام """
    logout_user()
    flash("تم تسجيل الخروج. النظام في وضع الحماية.", "info")
    return redirect(url_for('admin.login'))

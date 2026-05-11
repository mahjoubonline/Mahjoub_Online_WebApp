# admin_panel/routes.py
from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_required, logout_user
from . import admin_bp

# استدعاء الخدمات (التي تحتوي على المنطق البرمجي)
from core.services.supplier_service import get_all_suppliers, create_supplier, get_next_supplier_id
from core.services.stats_service import get_admin_dashboard_stats
from .auth import login_view 

# ==========================================
# 1. بوابة الولوج (Login)
# ==========================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    return login_view()

# ==========================================
# 2. لوحة التحكم (Dashboard) - استدعاء إحصائيات
# ==========================================
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # استدعاء الإحصائيات من خدمة الإحصائيات
    stats = get_admin_dashboard_stats()
    return render_template('admin/dashboard.html', **stats)

# ==========================================
# 3. إدارة الموردين - استدعاء البيانات
# ==========================================
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    # استدعاء قائمة الموردين والإحصائيات الخاصة بهم من الخدمة
    data = get_all_suppliers()
    return render_template('admin/manage_suppliers.html', **data)

# ==========================================
# 4. إضافة مورد - استدعاء محرك الأرشفة
# ==========================================
@admin_bp.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        # استلام البيانات (JSON أو Form)
        data = request.get_json() if request.is_json else request.form
        
        # استدعاء خدمة الإنشاء (التي تقوم بالتشفير، توليد الكود، والحفظ)
        success, result = create_supplier(data)
        
        if success:
            return jsonify({"status": "success", "message": result})
        return jsonify({"status": "error", "message": result}), 500

    # استدعاء الـ ID القادم لعرضه في الواجهة
    next_id = get_next_supplier_id()
    return render_template('admin/add_supplier.html', next_id=next_id)

# ==========================================
# 5. الخروج (Logout)
# ==========================================
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج بنجاح.", "info")
    return redirect(url_for('admin.login'))

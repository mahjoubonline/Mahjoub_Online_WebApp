# admin_panel/routes.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, logout_user, current_user
from core import db
from core.models.user import User
from core.models.supplier import Supplier
from datetime import datetime
import traceback

# 1. استيراد البلوبرنت
from . import admin_bp
from .auth import login_view 

# ==========================================
# 1. بوابة الولوج (The Login Gate)
# ==========================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    return login_view()

# ==========================================
# 2. غرفة القيادة (Dashboard)
# ==========================================
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        data = {
            'users_count': User.query.count() or 0,
            'suppliers_count': Supplier.query.count() or 0,
            'orders_count': 0, 
            'total_yer': db.session.query(db.func.sum(Supplier.balance_yer)).scalar() or 0.0,
            'total_sar': db.session.query(db.func.sum(Supplier.balance_sar)).scalar() or 0.0,
            'total_usd': db.session.query(db.func.sum(Supplier.balance_usd)).scalar() or 0.0,
            'now': datetime.now()
        }
        return render_template('admin/dashboard.html', **data)
    except Exception as e:
        error_details = traceback.format_exc()
        return render_template('admin/dashboard.html', error=f"⚠️ خطأ في الرادار: {error_details}")

# ==========================================
# 3. إدارة الموردين (Manage Suppliers)
# ==========================================
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    """عرض قائمة الموردين"""
    try:
        suppliers = Supplier.query.order_by(Supplier.id.desc()).all()
        stats = {
            'total': Supplier.query.count(),
            'active': Supplier.query.filter_by(status='active').count(),
            'sovereign': 0 
        }
        return render_template('admin/manage_suppliers.html', suppliers=suppliers, stats=stats)
    except Exception as e:
        return f"⚠️ خطأ في استعراض الموردين: {e}"

# ==========================================
# 4. إضافة مورد جديد (Add Supplier) - النسخة المعدلة والنهائية
# ==========================================
@admin_bp.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """فتح واجهة إضافة مورد جديد ومعالجة بروتوكول الحفظ الآمن"""
    if request.method == 'POST':
        try:
            # إصلاح خطأ 415: جعل الدالة تقبل JSON أو Form لضمان عدم الانهيار
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form

            if not data:
                return jsonify({"status": "error", "message": "عذراً قائد علي، لم يتم استلام بيانات صالحة للتعميد."}), 400

            # إنشاء كائن المورد وتعبئة البيانات من الطلب
            new_supplier = Supplier(
                name=data.get('name'),
                phone=data.get('phone'),
                location=data.get('location'),
                detailed_address=data.get('detailed_address'),
                wallet_number=data.get('wallet_number'),
                balance_yer=0.0,
                balance_sar=0.0,
                balance_usd=0.0,
                status='active'
            )
            
            db.session.add(new_supplier)
            db.session.commit()
            
            return jsonify({
                "status": "success", 
                "message": f"تم تعميد المورد ({new_supplier.name}) بنجاح في النظام الملكي."
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "status": "error", 
                "message": f"فشل بروتوكول التعميد التقني: {str(e)}"
            }), 500

    # عرض صفحة الإضافة عند طلب GET
    return render_template('admin/add_supplier.html')

# ==========================================
# 5. بروتوكول الخروج الآمن (Logout)
# ==========================================
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج. النظام في وضع الحماية.", "info")
    return redirect(url_for('admin.login'))

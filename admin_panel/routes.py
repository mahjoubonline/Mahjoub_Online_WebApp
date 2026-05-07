import os
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import or_, cast, String
from datetime import datetime

# الاستيراد من الهيكلية المعتمدة لترسانة محجوب أونلاين
from core.extensions import db 
from core.models.supplier import Supplier
from core.models.user import User

from . import admin_bp
from .auth import handle_admin_login

# --- 1. بروتوكول التحقق السيادي (حماية مركز القيادة) ---
def is_admin_sovereign():
    """ يضمن أن المؤسس علي محجوب فقط يمكنه الوصول. """
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 2. بوابة الدخول (The Gateway) ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_admin_sovereign(): 
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

# --- 3. مركز القيادة (Dashboard) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    
    try:
        suppliers_count = Supplier.query.count()
        users_count = User.query.count()
        
        try:
            from core.models.business import Order
            orders_count = Order.query.count()
        except Exception:
            orders_count = 0

        stats = {
            'suppliers_count': suppliers_count,
            'orders_count': orders_count,
            'users_count': users_count,
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return render_template('dashboard.html', **stats)
        
    except Exception as e:
        print(f"❌ Dashboard Stats Error: {str(e)}")
        return render_template('dashboard.html', suppliers_count=0, orders_count=0, users_count=0, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# --- 4. بروتوكول جلب تفاصيل المورد (للنافذة الجانبية) ---
@admin_bp.route('/api/supplier-details/<int:sup_id>')
@login_required
def api_supplier_details(sup_id):
    if not is_admin_sovereign():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    supplier = Supplier.query.get_or_404(sup_id)
    return jsonify(supplier.to_dict())

# --- 5. بروتوكول تعميد مورد جديد (The Creation Protocol) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if not is_admin_sovereign(): 
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            # إنشاء كائن المورد الجديد بناءً على بيانات النموذج
            new_supplier = Supplier(
                username=request.form.get('username'),
                password=request.form.get('password', '123456'), # كلمة مرور افتراضية
                owner_name=request.form.get('owner_name'),
                trade_name=request.form.get('trade_name'),
                activity_type=request.form.get('activity_type'),
                phone=request.form.get('phone'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                id_type=request.form.get('id_type'),
                id_card_number=request.form.get('id_card_number'),
                address_detail=request.form.get('address_detail'),
                bank_name=request.form.get('bank_name'),
                bank_acc=request.form.get('bank_acc'),
                status='active',
                tier='مبتدئ'
            )
            
            db.session.add(new_supplier)
            db.session.flush() # الحصول على الـ ID قبل الحفظ النهائي
            
            # نقش المعرف السيادي والمحفظة آلياً باستخدام دالة المودل
            new_supplier.mint_sovereign_id()
            
            db.session.commit()
            
            if is_ajax: 
                return jsonify({
                    'status': 'success', 
                    'message': f'تم تعميد المورد بنجاح بالمحفظة: {new_supplier.e_wallet}'
                })
            
            flash(f"تم إضافة المورد {new_supplier.trade_name} بنجاح", "success")
            return redirect(url_for('admin.manage_suppliers'))
            
        except Exception as e:
            db.session.rollback()
            if is_ajax:
                return jsonify({'status': 'error', 'message': f"فشل التعميد: {str(e)}"}), 400
            flash(f"خطأ في العملية: {str(e)}", "danger")

    # حساب المعرف القادم للعرض فقط في الواجهة
    last_s = Supplier.query.order_by(Supplier.id.desc()).first()
    next_id_val = (last_s.id + 1) if last_s else 1
    return render_template('add_supplier.html', next_id=f"963{next_id_val}")

# --- 6. تسجيل الخروج الآمن ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم إنهاء الجلسة السيادية بنجاح", "info")
    return redirect(url_for('admin.login'))

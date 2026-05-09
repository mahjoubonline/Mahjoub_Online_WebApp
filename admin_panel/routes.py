import os
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import or_
from datetime import datetime
from functools import wraps

# الاستيراد من الهيكلية المعتمدة لترسانة محجوب أونلاين
from core.extensions import db 
from core.models.supplier import Supplier, SupplierStaff
from core.models.user import User

from . import admin_bp
from .auth import handle_admin_login

# --- 1. بروتوكول التحقق السيادي (Sovereign Auth) ---
def is_admin_sovereign():
    """ يضمن أن المؤسس علي محجوب (أو من يحمل رتبة Admin) فقط يمكنه الوصول. """
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

def admin_api_required(f):
    """ تأمين الـ APIs لضمان أن الاستدعاءات تتم من داخل مركز القيادة فقط """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin_sovereign():
            return jsonify({"status": "error", "message": "Access Denied: Sovereign Auth Required"}), 403
        return f(*args, **kwargs)
    return decorated_function

# --- 2. بوابة الدخول ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_admin_sovereign(): 
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

# --- 3. مركز القيادة الإحصائي (Dashboard) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    
    try:
        stats = {
            'users_count': User.query.count() if User else 1,
            'suppliers_count': Supplier.query.count() if Supplier else 0,
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            from core.models.business import Order
            stats['orders_count'] = Order.query.count()
        except:
            stats['orders_count'] = 0

        return render_template('dashboard.html', **stats)
    except Exception as e:
        return render_template('dashboard.html', users_count=1, suppliers_count=0, orders_count=0, now="إيقاع النظام مستقر")

# --- 4. إدارة الموردين (عرض الواجهة الرئيسية للجدول) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    return render_template('manage_suppliers.html')

# --- 5. محرك البحث السيادي (API للترسانة) ---
@admin_bp.route('/api/suppliers/search')
@admin_api_required
def api_suppliers_search():
    query_str = request.args.get('q', '').strip()
    province = request.args.get('province', '')
    status = request.args.get('status', '')

    db_query = Supplier.query

    if query_str and query_str != '#':
        search_filter = or_(
            Supplier.owner_name.icontains(query_str),
            Supplier.trade_name.icontains(query_str),
            Supplier.username.icontains(query_str),
            Supplier.phone.icontains(query_str)
        )
        db_query = db_query.filter(search_filter)

    if province: db_query = db_query.filter(Supplier.province == province)
    if status: db_query = db_query.filter(Supplier.status == status)

    suppliers = db_query.order_by(Supplier.id.desc()).all()
    return jsonify([s.to_dict() for s in suppliers])

# --- 6. إضافة وتعمد مورد جديد ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if not is_admin_sovereign(): 
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            if Supplier.query.filter_by(username=request.form.get('username')).first():
                raise Exception("اسم المستخدم مسجل مسبقاً في الترسانة")

            new_supplier = Supplier(
                username=request.form.get('username'),
                owner_name=request.form.get('owner_name'),
                trade_name=request.form.get('trade_name'),
                phone=request.form.get('phone'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                tier=request.form.get('tier', 'مبتدئ'),
                status='active'
            )
            new_supplier.set_password(request.form.get('password', '123456'))
            
            db.session.add(new_supplier)
            db.session.flush() 
            new_supplier.mint_sovereign_id()
            db.session.commit()
            
            if is_ajax: 
                return jsonify({'status': 'success', 'message': 'تم تعميد المورد بنجاح'})
            return redirect(url_for('admin.manage_suppliers'))
            
        except Exception as e:
            db.session.rollback()
            if is_ajax: return jsonify({'status': 'error', 'message': str(e)}), 400
            flash(f"خطأ: {str(e)}", "danger")

    return render_template('add_supplier.html')

# --- 7. مركز إدارة الكيان (البروفايل السيادي) ---
@admin_bp.route('/supplier/<int:supplier_id>/profile')
@login_required
def supplier_profile(supplier_id):
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template('suppliers/supplier_profile.html', supplier=supplier)

# --- 8. محرك التحديث التلقائي (Auto-Save API) ---
@admin_bp.route('/supplier/<int:supplier_id>/update_field', methods=['POST'])
@admin_api_required
def update_supplier_field(supplier_id):
    """ 
    المعالج الذكي لتحديث أي حقل في قاعدة البيانات فوراً.
    يستقبل اسم الحقل والقيمة الجديدة من الواجهة.
    """
    data = request.get_json()
    field_name = data.get('field')
    new_value = data.get('value')
    
    supplier = Supplier.query.get_or_404(supplier_id)
    
    # قائمة الحقول المسموح بتعديلها لحماية أمن النظام
    allowed_fields = [
        'username', 'owner_name', 'trade_name', 'activity_type',
        'phone', 'province', 'district', 'address_detail',
        'bank_name', 'bank_acc', 'balance_yer', 'balance_sar', 'balance_usd',
        'tier', 'status'
    ]
    
    if field_name not in allowed_fields:
        return jsonify({"status": "error", "message": "محاولة تعديل حقل محظور"}), 403

    try:
        if hasattr(supplier, field_name):
            # تحويل القيم المالية لأرقام إذا لزم الأمر
            if 'balance' in field_name:
                try:
                    new_value = float(new_value) if new_value else 0.0
                except ValueError:
                    return jsonify({"status": "error", "message": "يجب إدخال قيمة رقمية صحيحة"}), 400
            
            setattr(supplier, field_name, new_value)
            db.session.commit()
            return jsonify({"status": "success", "message": f"تم تحديث {field_name} بنجاح"})
        else:
            return jsonify({"status": "error", "message": "الحقل غير موجود في قاعدة البيانات"}), 404
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# --- 9. إنهاء الجلسة السيادية ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تأمين الخروج من مركز القيادة.", "info")
    return redirect(url_for('admin.login'))

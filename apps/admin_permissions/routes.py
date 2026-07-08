# coding: utf-8
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
import secrets
import string

from apps.extensions import db
from apps.models.admin_staff_db import AdminStaff
from apps.models.supplier_staff_db import SupplierStaff
from apps.models.supplier_db import Supplier 

admin_permissions_bp = Blueprint('admin_permissions', __name__, template_folder='templates')

def is_admin():
    return current_user.is_authenticated and (getattr(current_user, 'role', '') in ['admin', 'Owner'])

def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))

# --- التحقق اللحظي من اسم المستخدم ---
@admin_permissions_bp.route('/admin/permissions/check-user', methods=['GET'])
@login_required
def check_user():
    username = request.args.get('username', '')
    if len(username) < 3: return jsonify({'available': False})
    
    # التحقق في كلا الجدولين
    exists = AdminStaff.query.filter_by(username=username).first() or \
             SupplierStaff.query.filter_by(username=username).first()
    return jsonify({'available': exists is None})

# --- التحقق اللحظي من رقم الهاتف ---
@admin_permissions_bp.route('/admin/permissions/check-phone', methods=['GET'])
@login_required
def check_phone():
    phone = request.args.get('phone', '')
    staff_type = request.args.get('type', 'admin')
    if len(phone) < 9: return jsonify({'available': False})
    
    model = AdminStaff if staff_type == 'admin' else SupplierStaff
    exists = model.query.filter_by(search_phone=phone[-9:]).first()
    return jsonify({'available': exists is None})

@admin_permissions_bp.route('/admin/permissions/roles', methods=['GET'])
@login_required
def roles_list():
    if not is_admin(): return redirect(url_for('admin_dashboard.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '')
    staff_type = request.args.get('type', 'admin')
    
    model = AdminStaff if staff_type == 'admin' else SupplierStaff
    query = model.query
    if search:
        query = query.filter((model.username.contains(search)) | (model.search_phone.contains(search[-9:])))
        
    pagination = query.order_by(model.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/permissions.html', staff=pagination.items, pagination=pagination, 
                           type_filter=staff_type, suppliers=Supplier.query.all())

@admin_permissions_bp.route('/admin/permissions/assign', methods=['POST'])
@login_required
def assign_permissions():
    if not is_admin(): return jsonify({'success': False, 'message': 'غير مصرح'})
    
    username = request.form.get('username')
    phone = request.form.get('phone')
    staff_type = request.form.get('type')
    supplier_id = request.form.get('supplier_id')
    
    password = generate_random_password() # كلمة مرور عشوائية للتعميد
    
    if staff_type == 'admin':
        new_staff = AdminStaff(username=username, role='worker')
    else:
        new_staff = SupplierStaff(username=username, role='worker', supplier_id=int(supplier_id))
    
    new_staff.phone = phone 
    new_staff.set_password(password)
    
    db.session.add(new_staff)
    try:
        db.session.commit()
        # إرجاع البيانات للـ AJAX لإظهار نافذة التعميد
        return jsonify({
            'success': True, 
            'username': username, 
            'password': password
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'خطأ في الحفظ'})

# --- المسارات الأخرى (reset_password و toggle_status) تبقى كما هي ---

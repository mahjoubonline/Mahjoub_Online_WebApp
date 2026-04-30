from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from core.models.user import User
from core.models.product import Product 
from core.models.supplier import Supplier 
from core import db # تأكد من استيراد قاعدة البيانات للحفظ

supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    if current_user.is_authenticated and current_user.role == 'supplier':
        return redirect(url_for('supplier_panel.supplier_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.role == 'supplier':
            # التحقق من حالة الموافقة السيادية
            if hasattr(user, 'is_approved') and user.is_approved():
                login_user(user)
                return redirect(url_for('supplier_panel.supplier_dashboard'))
            flash('حسابك في مرحلة التدقيق السيادي حالياً.', 'info')
        else:
            flash('بيانات الوصول غير معترف بها في الترسانة.', 'danger')
    return render_template('supplier_panel/supplier_login.html')

@supplier_bp.route('/dashboard')
@login_required
def supplier_dashboard():
    if not current_user.role == 'supplier':
        return redirect(url_for('main.index')) # توجيه للرئيسية إذا لم يكن مورداً

    # جلب بيانات المورد مع معالجة حالة عدم الوجود
    supplier_info = Supplier.query.filter_by(user_id=current_user.id).first()
    
    if not supplier_info:
        flash('لم يتم العثور على ملف مورد مرتبك بحسابك. تواصل مع الإدارة المركزية.', 'warning')
        products = []
    else:
        products = Product.query.filter_by(supplier_id=supplier_info.id).all()

    return render_template(
        'supplier_panel/dashboard.html', 
        supplier=supplier_info, 
        products=products
    )

# --- المسار الجديد الذي طلبته في القالب ---
@supplier_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.role == 'supplier':
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # منطق إضافة المنتج سيتم وضعه هنا لاحقاً
        flash('تم إرسال بيانات المنتج للترسانة بنجاح.', 'success')
        return redirect(url_for('supplier_panel.supplier_dashboard'))
        
    return render_template('supplier_panel/add_product.html')

@supplier_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم الخروج من بيئة التحكم بنجاح.', 'success')
    return redirect(url_for('supplier_panel.supplier_login'))

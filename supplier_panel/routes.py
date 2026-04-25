from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from core.models import Supplier, Product
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials # استدعاء ملف المنطق

# --- 1. مسار تسجيل الدخول اللامركزي ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and isinstance(current_user, Supplier):
        return redirect(url_for('supplier_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # استدعاء منطق التحقق الخارجي
        message, category, supplier = verify_supplier_credentials(username, password)
        
        flash(message, category)

        if supplier: # في حال النجاح (supplier ليس None)
            login_user(supplier)
            return redirect(url_for('supplier_panel.dashboard'))
            
    return render_template('supplier_login.html')

# --- 2. لوحة التحكم المحمية ---
@supplier_bp.route('/dashboard')
@login_required
def dashboard():
    if not isinstance(current_user, Supplier):
        logout_user()
        flash('هذا المسار مخصص لشركاء النجاح فقط.', 'danger')
        return redirect(url_for('supplier_panel.login'))
        
    my_products = Product.query.filter_by(supplier_id=current_user.id).all()
    return render_template('supplier_dashboard.html', products=my_products)

# --- 3. خروج المورد ---
@supplier_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح من بوابة الموردين.', 'info')
    return redirect(url_for('supplier_panel.login'))

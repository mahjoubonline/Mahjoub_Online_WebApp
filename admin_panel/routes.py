from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import admin_panel 
from core.models import User, Supplier, Product, db
from .utils import admin_required

# 1. بوابة الولوج السيادي (login.html)
@admin_panel.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and getattr(current_user, 'role', None) == 'admin':
        return redirect(url_for('admin_panel.admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, role='admin').first()

        if user and user.check_password(password):
            login_user(user)
            flash('تم تفعيل الولوج السيادي بنجاح.', 'success')
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('بيانات التحقق غير صحيحة.', 'danger')

    return render_template('login.html')

# 2. برج الرقابة (dashboard.html)
@admin_panel.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    stats = {
        's_count': Supplier.query.count(),
        'p_count': Product.query.count(),
        'orders_count': 0,
        'total_balance': 0.0
    }
    return render_template('dashboard.html', **stats)

# 3. إدارة الموردين (manage_suppliers.html)
@admin_panel.route('/suppliers')
@login_required
@admin_required
def manage_suppliers():
    suppliers = Supplier.query.all()
    return render_template('manage_suppliers.html', suppliers=suppliers)

# 4. تفاصيل المنتج (product_detail.html)
@admin_panel.route('/product/<int:id>')
@login_required
@admin_required
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

# 5. مراجعة المنتجات (product_review.html)
@admin_panel.route('/product-review')
@login_required
@admin_required
def product_review():
    # جلب المنتجات التي تنتظر المراجعة مثلاً
    pending_products = Product.query.filter_by(status='pending').all()
    return render_template('product_review.html', products=pending_products)

# 6. إدارة المحافظ المالية (wallets.html)
@admin_panel.route('/wallets')
@login_required
@admin_required
def manage_wallets():
    # هنا يتم عرض أرصدة الموردين والعملاء
    return render_template('wallets.html')

# 7. تسجيل الخروج
@admin_panel.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_panel.admin_login'))

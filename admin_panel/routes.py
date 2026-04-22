import os
from flask import Blueprint, render_template, request, redirect, url_for, flash

# تحديد المسار المطلق لمجلد templates لضمان وصول Flask إليه في Railway
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

# تعريف البلوبرنت
admin_bp = Blueprint('admin', __name__, template_folder=template_dir)

# --- المسارات (Routes) ---

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # هنا سنضيف منطق التحقق من قاعدة البيانات لاحقاً
        # حالياً سنقوم بالتحويل المباشر للوحة التحكم للتجربة
        return redirect(url_for('admin.dashboard'))
    return render_template('login.html')

@admin_bp.route('/admin/dashboard')
def dashboard():
    # سيقوم Flask بالبحث عن dashboard.html داخل admin_panel/templates
    return render_template('dashboard.html')

@admin_bp.route('/admin/wallets')
def wallets():
    return render_template('wallets.html')

@admin_bp.route('/admin/product-review')
def product_review():
    return render_template('product_review.html')

@admin_bp.route('/admin/order-routing')
def order_routing():
    return render_template('order_routing.html')

# مسار إضافي لتسجيل الخروج
@admin_bp.route('/admin/logout')
def logout():
    return redirect(url_for('admin.login'))

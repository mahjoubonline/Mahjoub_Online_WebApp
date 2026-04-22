from flask import Blueprint, render_template, request, redirect, url_for, flash
from core.models import User, db

# تعريف البلوبرنت الخاص بالإدارة
admin_bp = Blueprint('admin', __name__, 
                     template_folder='templates',
                     static_folder='static')

# 1. رابط صفحة الدخول
@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('admin_user')
        password = request.form.get('admin_pass')
        
        # هنا سنضع لاحقاً التحقق من قاعدة البيانات
        if username == "ali" and password == "123": # تجريبي حالياً
            return redirect(url_for('admin.dashboard'))
        else:
            return "بيانات الدخول غير صحيحة"
            
    return render_template('admin/login.html')

# 2. رابط لوحة التحكم (الداشبورد)
@admin_bp.route('/admin/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

# 3. رابط إدارة المحافظ (الذي طلبته)
@admin_bp.route('/admin/wallets')
def wallets():
    return render_template('admin/wallets.html')

# 4. روابط مراجعة المنتجات وتوجيه الطلبات
@admin_bp.route('/admin/product-review')
def product_review():
    return render_template('admin/product_review.html')

@admin_bp.route('/admin/order-routing')
def order_routing():
    return render_template('admin/order_routing.html')

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from admin_panel import admin_panel
from core.models import User, Supplier, Product, db
from core.utils.security import admin_required

# --- بوابة تسجيل الدخول (نظام الولوج السيادي) ---
@admin_panel.route('/login', methods=['GET', 'POST'])
def admin_login():
    # منع الدخول المتكرر إذا كان القائد مسجلاً بالفعل
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث في قاعدة بيانات Render
        user = User.query.filter_by(username=username, role='admin').first()

        if user and user.check_password(password):
            login_user(user)
            flash('تم تفعيل الولوج السيادي بنجاح.', 'success')
            return redirect(url_for('admin_panel.dashboard'))
        else:
            flash('فشل في التحقق من الهوية.. تأكد من معرف القائد أو مفتاح التشفير.', 'danger')

    return render_template('login.html')

# --- برج الرقابة المركزية (لوحة التحكم) ---
@admin_panel.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # إحصائيات حية من قاعدة بيانات Render
    stats = {
        'total_suppliers': Supplier.query.count(),
        'total_products': Product.query.count(),
        'pending_verifications': Supplier.query.filter_by(is_verified=False).count()
    }
    # ملاحظة: يتم تمرير stats إلى القالب لعرضها في الـ Dashboard
    return render_template('dashboard.html', stats=stats)

# --- إدارة شركاء الترسانة (الموردين) ---
@admin_panel.route('/manage-suppliers')
@login_required
@admin_required
def manage_suppliers():
    all_suppliers = Supplier.query.all()
    return render_template('manage_suppliers.html', suppliers=all_suppliers)

# --- نظام الاعتماد الفوري ---
@admin_panel.route('/verify-supplier/<int:supplier_id>')
@login_required
@admin_required
def verify_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    supplier.is_verified = True
    db.session.commit()
    flash(f'تم منح الاعتماد لمتجر: {supplier.store_name}.', 'success')
    return redirect(url_for('admin_panel.manage_suppliers'))

# --- إنهاء الجلسة الآمنة ---
@admin_panel.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم إغلاق البوابة السيادية بنجاح.', 'info')
    return redirect(url_for('admin_panel.admin_login'))

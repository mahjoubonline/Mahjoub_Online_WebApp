from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from core.models.supplier import Supplier
from core.models.product import Product
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials
from .decorators import sovereign_approval_required # استدعاء الحارس السيادي

# --- 1. مسار تسجيل الدخول اللامركزي ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    # إذا كان المستخدم مسجل دخوله بالفعل
    if current_user.is_authenticated:
        # إذا كان مورداً (يمتلك حقل wallet_balance) اذهب للداشبورد
        if hasattr(current_user, 'wallet_balance'):
            return redirect(url_for('supplier_panel.dashboard'))
        # إذا كان أدمن يحاول الدخول لصفحة المورد، سجل خروجه أولاً
        else:
            logout_user()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('يرجى ملء كافة الحقول السيادية للدخول.', 'warning')
            return render_template('supplier_login.html')

        # استدعاء المحقق الخارجي للتأكد من قاعدة البيانات
        message, category, supplier = verify_supplier_credentials(username, password)
        
        if supplier: 
            login_user(supplier)
            flash(f'أهلاً بك يا {supplier.name} في نظام الترسانة', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash(message, category)
            
    return render_template('supplier_login.html')

# --- 2. لوحة التحكم المحمية (الترسانة) ---
@supplier_bp.route('/dashboard')
@login_required
@sovereign_approval_required # 🛡️ الحارس الأول: يمنع المورد غير المعتمد من الدخول
def dashboard():
    # 🛡️ الحارس الثاني: فحص أمني للتأكد أن المستخدم "مورد" وليس "أدمن"
    if not hasattr(current_user, 'wallet_balance'):
        logout_user()
        flash('عذراً، هذه المنطقة مخصصة لشركاء النجاح (الموردين) فقط.', 'danger')
        return redirect(url_for('supplier_panel.login'))
        
    # جلب منتجات المورد المرتبطة برقم محفظته
    my_products = Product.query.filter_by(supplier_id=current_user.id).all()
    
    return render_template('supplier_dashboard.html', products=my_products)

# --- 3. خروج المورد ---
@supplier_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تأمين الجلسة وتسجيل الخروج من الترسانة.', 'info')
    return redirect(url_for('supplier_panel.login'))

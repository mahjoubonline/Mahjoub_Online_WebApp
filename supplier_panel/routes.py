from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials
from .decorators import sovereign_approval_required 

# --- 1. مسار تسجيل الدخول ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if hasattr(current_user, 'wallet_balance'):
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            logout_user() 

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('يرجى ملء كافة الحقول السيادية للدخول.', 'warning')
            return render_template('supplier_login.html')

        message, category, supplier = verify_supplier_credentials(username, password)
        
        if supplier: 
            login_user(supplier)
            flash(f'تم الولوج بنجاح.. أهلاً بك يا {supplier.name}', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash(message, category)
            
    return render_template('supplier_login.html')

# --- 2. لوحة التحكم (التصحيح هنا) ---
@supplier_bp.route('/dashboard')
@login_required
@sovereign_approval_required 
def dashboard():
    from core.models.product import Product
    
    try:
        if not hasattr(current_user, 'wallet_balance'):
            logout_user()
            flash('عذراً، هذه المنطقة مخصصة لشركاء النجاح فقط.', 'danger')
            return redirect(url_for('supplier_panel.login'))
            
        # جلب المنتجات مع حماية ضد أخطاء قاعدة البيانات
        try:
            # تأكد أن الموديل يحتوي على الحقل supplier_id
            my_products = Product.query.filter_by(supplier_id=current_user.id).all()
        except:
            my_products = []
            
        # التصحيح: اسم الملف هو dashboard.html كما أرسلته لي
        return render_template('dashboard.html', products=my_products)
        
    except Exception as e:
        print(f"❌ خطأ داخلي في لوحة المورد: {e}")
        # عرض الخطأ بشكل أوضح للتصحيح
        return f"خطأ في النظام (500): {str(e)}", 500

# --- 3. صفحة الانتظار ---
@supplier_bp.route('/waiting-room')
@login_required
def waiting_room():
    if hasattr(current_user, 'is_approved') and current_user.is_approved:
        return redirect(url_for('supplier_panel.dashboard'))
    
    return render_template('waiting_approval.html')

# --- 4. الخروج ---
@supplier_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تأمين الجلسة وتشفير الخروج بنجاح.', 'info')
    return redirect(url_for('supplier_panel.login'))

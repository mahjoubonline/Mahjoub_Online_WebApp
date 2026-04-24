from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from core import db
from core.models import Supplier, Product
from . import supplier_bp  # استيراد البلوبرنت المُعرّف في __init__.py

# --- 1. مسار تسجيل الدخول للمورد (بالاسم العربي) ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    # إذا كان المستخدم مسجل دخوله مسبقاً، يوجهه للوحة التحكم
    if current_user.is_authenticated:
        if isinstance(current_user, Supplier):
            return redirect(url_for('supplier_panel.dashboard'))
    
    if request.method == 'POST':
        # استقبال 'username' العربي من الفورم الجديد
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث في قاعدة البيانات عن المورد باسمه العربي
        supplier = Supplier.query.filter_by(name=username).first()
        
        if supplier and supplier.password == password:
            login_user(supplier)
            flash(f'مرحباً بك يا {supplier.name} في بوابة شركاء النجاح', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash('اسم المورد أو كلمة المرور غير صحيحة، يرجى المحاولة مرة أخرى.', 'danger')
            
    return render_template('login.html')

# --- 2. لوحة تحكم المورد (الإحصائيات والمحفظة) ---
@supplier_bp.route('/')
@supplier_bp.route('/dashboard')
@login_required
def dashboard():
    # التحقق الأمني: التأكد أن المستخدم هو مورد وليس مسؤول (Admin)
    if not isinstance(current_user, Supplier):
        logout_user()
        flash('هذه البوابة مخصصة لشركاء النجاح فقط.', 'warning')
        return redirect(url_for('supplier_panel.login'))
        
    # جلب منتجات هذا المورد فقط
    my_products = Product.query.filter_by(supplier_id=current_user.id).all()
    return render_template('dashboard.html', products=my_products)

# --- 3. نافذة رفع منتج جديد (سعر التكلفة) ---
@supplier_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not isinstance(current_user, Supplier):
        return redirect(url_for('supplier_panel.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        cost_price = request.form.get('cost_price')
        image_url = request.form.get('image_url')
        
        # إنشاء كائن المنتج وربطه بصاحب الحساب الحالي
        new_product = Product(
            name=name,
            description=description,
            original_price=float(cost_price) if cost_price else 0.0,
            sale_price=0.0,  # يحدده الأدمن لاحقاً
            image_url=image_url,
            supplier_id=current_user.id,
            status='pending', # قيد المراجعة السيادية
            is_synced=False   # لم يظهر في المتجر العام بعد
        )
        
        try:
            db.session.add(new_product)
            db.session.commit()
            flash('✅ تم إرسال المنتج للمراجعة بنجاح.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'⚠️ حدث خطأ فني أثناء الحفظ: {str(e)}', 'danger')

    return render_template('add_product.html')

# --- 4. تسجيل الخروج ---
@supplier_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج من بوابة الموردين بنجاح.', 'info')
    return redirect(url_for('supplier_panel.login'))

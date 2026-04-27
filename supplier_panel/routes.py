from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials
from .decorators import sovereign_approval_required 
from core import db
from core.models import Product, Supplier, User # استدعاء الموديلات الموحدة
from core.qumra_connector import QumraConnector # المحرك الجديد

# إنشاء نسخة من موصل قمرة لاستخدامه في جلب الأقسام
qumra = QumraConnector()

# --- 1. بوابة الدخول للموردين ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if session.get('user_type') == 'supplier':
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            logout_user()
            session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('يرجى إدخال بيانات الهوية السيادية للمورد.', 'warning')
            return render_template('supplier_panel/login.html')

        # التحقق من الهوية (يرجع كائن User)
        message, category, user = verify_supplier_credentials(username, password)
        
        if user and user.role == 'supplier': 
            session.permanent = True
            session['user_type'] = 'supplier' 
            login_user(user)
            # جلب اسم المورد من البروفايل المرتبط
            supplier_name = user.supplier_profile.trade_name if user.supplier_profile else user.username
            flash(f'مرحباً بك يا {supplier_name} في منصة محجوب أونلاين.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash(message or "عذراً، هذه البوابة للموردين فقط.", 'danger')
            
    return render_template('supplier_panel/login.html')

# --- 2. لوحة تحكم المورد (الترسانة المالية) ---
@supplier_bp.route('/dashboard')
@login_required
@sovereign_approval_required 
def dashboard():
    if session.get('user_type') != 'supplier':
        logout_user()
        return redirect(url_for('supplier_panel.login'))
        
    try:
        # الوصول لبيانات المورد المالية عبر العلاقة backref
        supplier_data = current_user.supplier_profile
        # جلب المنتجات التابعة لهذا المورد حصراً
        my_products = Product.query.filter_by(supplier_id=supplier_data.id).all()
        
        return render_template('supplier_panel/dashboard.html', 
                               supplier=supplier_data, 
                               products=my_products)
    except Exception as e:
        print(f"⚠️ خطأ في استعراض البيانات السيادية: {e}")
        return f"خطأ تقني: {str(e)}", 500

# --- 3. إضافة منتج جديد (بوابة التوريد) ---
@supplier_bp.route('/add-product', methods=['GET', 'POST'])
@login_required
@sovereign_approval_required
def add_product():
    # جلب الأقسام (Collections) مباشرة من محرك قمرة الجديد
    # ملاحظة: سنفترض وجود دالة get_collections في الموصل
    collections = qumra.get_order_details('collections') # تجريبي

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        cost_price = request.form.get('cost_price')
        
        if not name or not cost_price:
            flash('اسم المنتج وسعر التكلفة حقول إلزامية للتعميد.', 'danger')
            return redirect(request.url)

        try:
            new_product = Product(
                name=name,
                description=description,
                cost_price=float(cost_price),
                supplier_id=current_user.supplier_profile.id,
                is_active=False # يبقى غير نشط حتى تعمده أنت من لوحة الإدارة
            )
            
            db.session.add(new_product)
            db.session.commit()
            flash('✅ تم رفع المنتج بنجاح. سيتم مراجعته وتعميده من قبل القائد علي محجوب.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'⚠️ فشل في حفظ البيانات: {str(e)}', 'danger')

    return render_template('supplier_panel/add_product.html', collections=collections)

# --- 4. تسجيل الخروج ---
@supplier_bp.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('supplier_panel.login'))

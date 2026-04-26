from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials
from .decorators import sovereign_approval_required 
from core import db
from core.models.product import Product
from core.models.supplier import Supplier
# استيراد محرك جلب الأقسام من قمرة ليعرضها للمورد عند إضافة منتج
from services.qumra_handler import fetch_qumra_collections

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
            # التعديل هنا: إضافة مسار المجلد الفرعي
            return render_template('supplier_panel/supplier_login.html')

        message, category, supplier = verify_supplier_credentials(username, password)
        
        if supplier: 
            session.permanent = True
            session['user_type'] = 'supplier' 
            login_user(supplier)
            flash(f'مرحباً بك يا {supplier.name} في منصة محجوب أونلاين.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash(message, category)
            
    # التعديل هنا: التوجه للمجلد الفرعي حسب الصورة
    return render_template('supplier_panel/supplier_login.html')

# --- 2. لوحة تحكم المورد ---
@supplier_bp.route('/dashboard')
@login_required
@sovereign_approval_required 
def dashboard():
    if session.get('user_type') != 'supplier':
        session.clear()
        logout_user()
        return redirect(url_for('supplier_panel.login'))
        
    try:
        my_products = Product.query.filter_by(supplier_id=current_user.id).all()
        # التعديل هنا: التوجه للمجلد الفرعي
        return render_template('supplier_panel/dashboard.html', products=my_products)
    except Exception as e:
        return f"خطأ في استعراض البيانات السيادية: {str(e)}", 500

# --- 3. إضافة منتج جديد ---
@supplier_bp.route('/add-product', methods=['GET', 'POST'])
@login_required
@sovereign_approval_required
def add_product():
    if session.get('user_type') != 'supplier':
        return redirect(url_for('supplier_panel.login'))

    collections = fetch_qumra_collections()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        collection_id = request.form.get('collection_id')
        cost_price = request.form.get('cost_price')
        currency = request.form.get('currency', 'YER') 
        
        if not name or not cost_price:
            flash('اسم المنتج وسعر التكلفة حقول إلزامية للتعميد.', 'danger')
            return redirect(request.url)

        try:
            new_product = Product(
                name=name,
                description=description,
                q_collection_id=collection_id,
                cost_price=float(cost_price),
                currency=currency,
                supplier_id=current_user.id,
                status='pending' 
            )
            
            db.session.add(new_product)
            db.session.commit()
            flash('✅ تم رفع المنتج بنجاح. سيتم مراجعته ونشره قريباً.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'⚠️ فشل في حفظ البيانات: {str(e)}', 'danger')

    # التعديل هنا: التوجه للمجلد الفرعي
    return render_template('supplier_panel/add_product.html', collections=collections)

# --- 4. غرفة الانتظار ---
@supplier_bp.route('/waiting-room')
@login_required
def waiting_room():
    supplier = Supplier.query.get(current_user.id)
    if supplier and supplier.is_approved:
        return redirect(url_for('supplier_panel.dashboard'))
    
    # التعديل هنا: التوجه للمجلد الفرعي
    return render_template('supplier_panel/waiting_approval.html')

# --- 5. الخروج ---
@supplier_bp.route('/logout')
@login_required
def logout():
    session.pop('user_type', None)
    session.clear()
    logout_user()
    return redirect(url_for('supplier_panel.login'))

from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import admin_bp
from core import db
from core.models.user import User
from core.models.supplier import Supplier
from core.models.product import Product
from services.qumra_handler import create_qumra_product

# --- 1. مدخل برج الرقابة (تسجيل الدخول) ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and session.get('user_type') == 'admin':
        return redirect(url_for('admin_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن القائد (ali_mahjoub)
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password: # يفضل تشفيرها لاحقاً
            session.clear() # تطهير الجلسة من أي أثر للموردين
            session['user_type'] = 'admin'
            login_user(user)
            flash(f'أهلاً بك يا قائد {user.username} في برج الرقابة.', 'success')
            return redirect(url_for('admin_panel.dashboard'))
        else:
            flash('بيانات الدخول غير صحيحة، الوصول للمنطقة السيادية مرفوض.', 'danger')

    return render_template('admin_login.html')

# --- 2. لوحة التحكم المركزية ---
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_panel.login'))
        
    # جلب إحصائيات سريعة للوحة التحكم
    total_suppliers = Supplier.query.count()
    pending_products = Product.query.filter_by(status='pending').all()
    return render_template('admin_dashboard.html', 
                           suppliers_count=total_suppliers, 
                           products=pending_products)

# --- 3. تعميد ونشر المنتج إلى قمرة (النشر السيادي) ---
@admin_bp.route('/approve-product/<int:product_id>', methods=['POST'])
@login_required
def approve_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # استقبال السعر النهائي (البيع) الذي يحدده علي محجوب
    sale_price = request.form.get('sale_price')
    
    if not sale_price:
        flash('يجب تحديد سعر البيع قبل التعميد.', 'warning')
        return redirect(url_for('admin_panel.dashboard'))

    try:
        # 🚀 إرسال المنتج إلى قمرة عبر المحرك الخفيف
        qumra_response = create_qumra_product(
            name=product.name,
            description=product.description or "منتج معمد من محجوب أونلاين",
            price=float(sale_price),
            collection_id=product.q_collection_id
        )

        if qumra_response and 'data' in qumra_response:
            q_id = qumra_response['data']['productCreate']['product']['id']
            
            # تحديث حالة المنتج محلياً وربطه بمعرف قمرة
            product.status = 'active'
            product.q_product_id = q_id
            db.session.commit()
            
            flash(f'✅ تم تعميد المنتج ونشره في قمرة بنجاح بالمعرف: {q_id}', 'success')
        else:
            flash('❌ فشل النشر في قمرة، يرجى التحقق من التوكن أو الرابط.', 'danger')
            
    except Exception as e:
        db.session.rollback()
        flash(f'⚠️ خطأ فني أثناء التعميد: {str(e)}', 'danger')

    return redirect(url_for('admin_panel.dashboard'))

# --- 4. خروج القائد ---
@admin_bp.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('admin_panel.login'))

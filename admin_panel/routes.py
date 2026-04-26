from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from core import db
from services.qumra_handler import query_qumra # المحرك السيادي للربط مع قمرة
import os

# 1. إعداد المسار والـ Blueprint
# تم ضبط المجلدات لضمان وصول النظام للقوالب (Templates) الخاصة بالإدارة
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

# --- معالج السياق (Sidebar Counts) ---
@admin_bp.context_processor
def inject_counts():
    from core.models.supplier import Supplier
    try:
        # حساب الموردين الذين ينتظرون التفعيل لظهور الإشعار في القائمة الجانبية
        pending_count = Supplier.query.filter_by(is_approved=False).count()
        return dict(pending_suppliers_count=pending_count)
    except:
        return dict(pending_suppliers_count=0)

# 2. لوحة التحكم (برج الرقابة الرئيسي)
@admin_bp.route('/', strict_slashes=False)
@admin_bp.route('/dashboard') # إضافة مسار صريح للداشبورد
@login_required
def dashboard():
    # التأكد من أن الهوية هي "أدمن" حصراً لمنع الموردين من دخول هذا المسار
    if session.get('user_type') != 'admin':
        logout_user()
        return redirect(url_for('admin_panel.login'))

    from core.models.supplier import Supplier
    from core.models.product import Product
    try:
        s_count = Supplier.query.count()
        p_count = Product.query.count()
        latest_suppliers = Supplier.query.order_by(Supplier.created_at.desc()).limit(5).all()
        # تصحيح المسار ليشمل المجلد الفرعي admin_panel كما في صورك
        return render_template('admin_panel/dashboard.html', s_count=s_count, p_count=p_count, latest_suppliers=latest_suppliers)
    except Exception as e:
        print(f"Error in dashboard: {e}")
        return render_template('admin_panel/dashboard.html', s_count=0, p_count=0, latest_suppliers=[])

# 3. بوابة مراجعة المنتجات (Sync Room)
@admin_bp.route('/sync_now', strict_slashes=False)
@login_required
def sync_now():
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_panel.login'))

    from core.models.product import Product
    # جلب المنتجات التي رفعها الموردون وحالتها "pending" فقط لمراجعتها ونشرها
    pending_products = Product.query.filter_by(status='pending').all()
    return render_template('admin_panel/product_review.html', products=pending_products)

# 4. النشر السيادي: إرسال البيانات لقمرة (Direct Push)
@admin_bp.route('/product/approve/<int:product_id>', methods=['POST'])
@login_required
def approve_product(product_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_panel.login'))

    from core.models.product import Product
    product = Product.query.get_or_404(product_id)
    
    # السعر النهائي بالريال السعودي الذي يحدده علي محجوب
    final_price_sar = request.form.get('final_price')

    # بناء طلب النشر المباشر عبر GraphQL قمرة
    mutation = """
    mutation CreateProduct($input: ProductInput!) {
      productCreate(input: $input) {
        product { id name }
        userErrors { field message }
      }
    }
    """
    
    variables = {
        "input": {
            "name": product.name,
            "descriptionHtml": product.description or "",
            "collections": [product.q_collection_id] if product.q_collection_id else [],
            "variants": [{
                "price": float(final_price_sar),
                "inventoryQuantity": 10 
            }]
        }
    }

    try:
        result = query_qumra(mutation, variables)
        
        if result and 'data' in result and result['data']['productCreate']['product']:
            product.q_product_id = result['data']['productCreate']['product']['id']
            product.status = 'active'
            product.is_synced = True
            db.session.commit()
            
            flash(f'✅ تم النشر بنجاح. معرف المنتج في قمرة: {product.q_product_id}', 'success')
        else:
            error_msg = "خطأ في الاتصال بسيرفر قمرة"
            if result and 'data' in result and result['data']['productCreate']['userErrors']:
                error_msg = result['data']['productCreate']['userErrors'][0]['message']
            flash(f'❌ فشل النشر: {error_msg}', 'danger')
            
    except Exception as e:
        db.session.rollback()
        flash(f'⚠️ خطأ تقني أثناء التعميد: {str(e)}', 'danger')

    return redirect(url_for('admin_panel.sync_now'))

# 5. تسجيل الدخول (القائد علي محجوب)
@admin_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated and session.get('user_type') == 'admin':
        return redirect(url_for('admin_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        from core.models.user import User
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session.clear() 
            session['user_type'] = 'admin'
            login_user(user)
            flash('أهلاً بك أيها القائد في برج الرقابة السيادي', 'success')
            return redirect(url_for('admin_panel.dashboard'))
        else:
            flash('بيانات الولوج غير صحيحة، الوصول للمنطقة السيادية مرفوض.', 'danger')
            
    return render_template('admin_panel/login.html')

# 6. تسجيل الخروج وتطهير الجلسة
@admin_bp.route('/logout')
@login_required
def logout():
    session.pop('user_type', None)
    session.clear()
    logout_user()
    return redirect(url_for('admin_panel.login'))

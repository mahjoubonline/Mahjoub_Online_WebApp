from flask import Blueprint, render_template, request
from core.models import Product, Supplier  # استيراد من الترسانة المركزية

# تعريف البلوبرنت الخاص بالواجهة العامة
main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    """
    الصفحة الرئيسية: تعرض أحدث المنتجات المضافة في المنصة.
    """
    # جلب آخر 8 منتجات نشطة فقط لضمان سرعة التحميل
    featured_products = Product.query.filter_by(is_active=True).order_multiplier(Product.id.desc()).limit(8).all()
    return render_template('main/index.html', products=featured_products)

@main_bp.route('/shop')
def shop():
    """
    صفحة المتجر الكاملة مع إمكانية الفلترة حسب الفئة.
    """
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category, is_active=True).all()
    else:
        products = Product.query.filter_by(is_active=True).all()
    
    return render_template('main/shop.html', products=products)

@main_bp.route('/product/<int:product_id>')
def product_details(product_id):
    """
    صفحة تفاصيل المنتج الواحد.
    """
    product = Product.query.get_or_404(product_id)
    # جلب بيانات المورد صاحب المنتج لعرضها بجانب المنتج
    supplier = Supplier.query.get(product.supplier_id)
    return render_template('main/product_details.html', product=product, supplier=supplier)

from flask import render_template, request
from . import main_bp  # استيراد البلوبرنت من ملف __init__.py المحلي
from core.models.product import Product  # استيراد دقيق للموديلات من الترسانة المركزية
from core.models.supplier import Supplier

@main_bp.route('/')
def index():
    """
    الصفحة الرئيسية: تعرض أحدث المنتجات المضافة في المنصة.
    """
    try:
        # جلب آخر 8 منتجات نشطة لضمان سرعة التحميل وأداء عالي للمنصة
        # تم تصحيح order_by لترتيب المنتجات من الأحدث إلى الأقدم
        featured_products = Product.query.filter_by(is_active=True).order_by(Product.id.desc()).limit(8).all()
    except Exception as e:
        print(f"Error fetching products: {e}")
        featured_products = []
        
    return render_template('main/index.html', products=featured_products)

@main_bp.route('/shop')
def shop():
    """
    صفحة المتجر الكاملة مع إمكانية الفلترة حسب الفئة.
    """
    category = request.args.get('category')
    if category:
        # فلترة المنتجات حسب الفئة المختارة (مثلاً: ملابس، إلكترونيات)
        products = Product.query.filter_by(category=category, is_active=True).all()
    else:
        # عرض كافة المنتجات النشطة في حال عدم اختيار فئة
        products = Product.query.filter_by(is_active=True).all()
    
    return render_template('main/shop.html', products=products)

@main_bp.route('/product/<int:product_id>')
def product_details(product_id):
    """
    صفحة تفاصيل المنتج الواحد: تربط المنتج بالمورد المسؤول عنه.
    """
    # جلب المنتج أو إظهار صفحة 404 في حال عدم وجوده
    product = Product.query.get_or_404(product_id)
    
    # جلب بيانات المورد صاحب المنتج لعرضها في صفحة التفاصيل
    supplier = Supplier.query.get(product.supplier_id)
    
    return render_template('main/product_details.html', product=product, supplier=supplier)

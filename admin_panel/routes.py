from flask import Blueprint, render_template, request

# تعريف البلوبرنت مع تحديد مجلد القوالب بدقة
admin_bp = Blueprint('admin_panel', __name__, template_folder='templates')

# 1. مسار لوحة التحكم (الداتشبورد)
@admin_bp.route('/', strict_slashes=False)
def dashboard():
    # استيراد المودلز هنا يمنع الخطأ الدائري عند الإقلاع
    from core.models import Supplier, Product
    try:
        s_count = Supplier.query.count()
        p_count = Product.query.count()
        return render_template('dashboard.html', s_count=s_count, p_count=p_count)
    except Exception:
        # إذا كانت القاعدة فارغة أو بها مشكلة، يفتح الداتشبورد بأرقام صفرية
        return render_template('dashboard.html', s_count=0, p_count=0)

# 2. مسار عرض المنتجات (المزامنة اللحظية)
@admin_bp.route('/sync_now', strict_slashes=False)
def sync_now():
    try:
        from core.qumra_sync import qumra_manager
        live_products = qumra_manager.fetch_live_products(limit=15)
        return render_template('product_review.html', products=live_products)
    except Exception as e:
        print(f"⚠️ خطأ في المزامنة: {e}")
        return render_template('product_review.html', products=[])

# 3. مسار صفحة الدخول
@admin_bp.route('/login', strict_slashes=False)
def login():
    return render_template('login.html')

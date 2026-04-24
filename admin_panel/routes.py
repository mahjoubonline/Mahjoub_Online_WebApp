from flask import Blueprint, render_template, request
from core.qumra_sync import qumra_manager  # استيراد المحرك اللحظي
from core.models import Supplier, Product

# تعريف البلوبرنت
admin_bp = Blueprint('admin_panel', __name__, template_folder='templates')

# 1. لوحة التحكم (الرئيسية)
@admin_bp.route('/', strict_slashes=False)
def dashboard():
    try:
        # جلب إحصائيات سريعة من القاعدة المحلية (رندر)
        suppliers_count = Supplier.query.count()
        products_count = Product.query.count()
        
        # عرض واجهة الإدارة البسيطة
        return render_template('dashboard.html', s_count=suppliers_count, p_count=products_count)
    except Exception:
        # إذا لم تكن الجداول موجودة بعد، نعرض أرقام صفرية
        return render_template('dashboard.html', s_count=0, p_count=0)

# 2. عرض المنتجات اللحظي من قمرة (بدون تخزين)
@admin_bp.route('/sync_now', strict_slashes=False)
def sync_now():
    # استدعاء الوظيفة اللحظية التي تجلب البيانات والصور
    live_products = qumra_manager.fetch_live_products(limit=15)
    
    # إرسال البيانات لملف الـ HTML الذي صممناه (product_review.html)
    return render_template('product_review.html', products=live_products)

# 3. عرض قائمة الموردين من قاعدة رندر
@admin_bp.route('/suppliers', strict_slashes=False)
def list_suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers_list.html', suppliers=suppliers)

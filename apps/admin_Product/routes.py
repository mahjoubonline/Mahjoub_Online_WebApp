# 📂 apps/admin_Product/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from sqlalchemy.orm import lazyload
from apps.models.product_db import Product
from apps.extensions import db
# تم تعديل الاستيراد هنا ليتناسب مع الكلاس
from apps.services.graphql_client import QomrahGraphQLClient

# تعريف البلوبرينت
admin_product_bp = Blueprint(
    'admin_product', 
    __name__, 
    template_folder='templates'
)

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    """عرض قائمة المنتجات بنظام الصفحات"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = Product.query.options(lazyload(Product.supplier))\
        .order_by(Product.created_at.desc())\
        .paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
    
    return render_template(
        'admin/admin_Product.html', 
        products=pagination.items,
        pagination=pagination
    )

@admin_product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """مسار آمن يعرض قائمة المنتجات"""
    return redirect(url_for('admin_product.manage_products'))

@admin_product_bp.route('/sync', methods=['POST'])
@login_required
def sync_products():
    """مسار المزامنة الفعلي الذي يستخدم كلاس QomrahGraphQLClient"""
    try:
        # 1. جلب المنتجات باستخدام الكلاس (بافتراض إضافة دالة fetch_products للكلاس)
        # ملاحظة: تأكد أنك أضفت دالة fetch_products داخل كلاس QomrahGraphQLClient في ملف graphql_client.py
        products_data = QomrahGraphQLClient.fetch_products()
        
        # 2. تحديث قاعدة البيانات
        for item in products_data:
            # البحث عن المنتج بـ qid
            product = Product.query.filter_by(qid=str(item['_id'])).first()
            
            if not product:
                # إنشاء منتج جديد
                new_product = Product(
                    qid=str(item['_id']),
                    title=item['title'],
                    supplier_id=1, 
                    sku=item.get('sku')
                )
                new_product.cost_price = item.get('price') 
                db.session.add(new_product)
            else:
                # تحديث البيانات الموجودة
                product.title = item['title']
                product.cost_price = item.get('price')
        
        db.session.commit()
        return jsonify({"status": "success", "message": f"تمت مزامنة {len(products_data)} منتج بنجاح!"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

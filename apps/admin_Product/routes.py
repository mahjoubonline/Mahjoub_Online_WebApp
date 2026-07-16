# coding: utf-8
# 📂 apps/admin_Product/routes.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from apps.models.product_db import Product
from apps.extensions import db
from apps.services.graphql_client import QomrahGraphQLClient

admin_product_bp = Blueprint(
    'admin_product_bp', 
    __name__, 
    template_folder='templates'
)

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Product.query.order_by(Product.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'admin/admin_Product.html', 
        products=pagination.items,
        pagination=pagination
    )

@admin_product_bp.route('/proxy-sync', methods=['POST'])
@login_required
def proxy_sync():
    """الوكيل لجلب القوائم (Menus) وتصحيح المسارات بناءً على الـ API"""
    
    # الاستعلام المحدث بناءً على اسم العملية في Apollo
    query = """
    query { 
        findAllMenus { 
            data { 
                _id 
                title 
                price 
                sku 
            } 
        } 
    }
    """
    
    data = QomrahGraphQLClient.execute_query(query)
    
    if data is None or 'findAllMenus' not in data:
        return jsonify({
            "status": "error", 
            "message": "فشل جلب البيانات. تأكد من هيكل الاستعلام."
        }), 500
        
    # هنا نقوم بإعادة البيانات الموجودة داخل 'data' التابعة لـ 'findAllMenus'
    # وهذا يتطابق مع ما سنعالجه في save_sync
    return jsonify({"status": "success", "data": data['findAllMenus']['data']})

@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    """حفظ البيانات المجلوبة"""
    try:
        data = request.json
        # يجب أن تأتي البيانات من الطلب القادم من الفرونت-إند (الذي استلم الـ data)
        products_data = data.get('products', [])
        
        if not products_data:
            return jsonify({"status": "error", "message": "لا توجد منتجات للمزامنة"})

        count = 0
        for item in products_data:
            qid = str(item.get('_id'))
            product = Product.query.filter_by(qid=qid).first()
            
            try:
                price = float(item.get('price', 0))
            except (ValueError, TypeError):
                price = 0.0

            if not product:
                new_product = Product(
                    qid=qid,
                    title=item.get('title', 'منتج غير معرف'),
                    sku=item.get('sku', 'N/A'),
                    cost_price=price
                )
                db.session.add(new_product)
                count += 1
            else:
                product.title = item.get('title', product.title)
                product.cost_price = price
                product.sku = item.get('sku', product.sku)
        
        db.session.commit()
        return jsonify({
            "status": "success", 
            "message": f"تمت المزامنة: إضافة {count} وتحديث الباقي."
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"خطأ: {str(e)}"}), 500

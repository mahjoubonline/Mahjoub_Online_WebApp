# coding: utf-8
# 📂 apps/admin_Product/routes.py

import os
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy.orm import lazyload
from apps.models.product_db import Product
from apps.extensions import db
from apps.services.graphql_client import QomrahGraphQLClient

admin_product_bp = Blueprint('admin_product_bp', __name__, template_folder='templates')

@admin_product_bp.route('/', methods=['GET'])
@login_required
def manage_products():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Product.query.options(lazyload(Product.supplier))\
        .order_by(Product.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/admin_Product.html', products=pagination.items, pagination=pagination)

@admin_product_bp.route('/proxy-sync', methods=['POST'])
@login_required
def proxy_sync():
    # الاستعلام لجلب المنتجات
    query = """
    query { 
        findAllProducts(page: 1, limit: 100) { 
            items { _id title price sku } 
        } 
    }
    """
    data = QomrahGraphQLClient.execute_query(query)
    
    if data is None:
        return jsonify({"status": "error", "message": "تعذر الاتصال بخدمة محجوب للمزامنة"}), 500
        
    return jsonify({"status": "success", "data": data})

@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    try:
        data = request.json
        products_data = data.get('data', {}).get('findAllProducts', {}).get('items', [])
        
        if not products_data:
            return jsonify({"status": "error", "message": "لا توجد بيانات صالحة للمزامنة"})

        count = 0
        for item in products_data:
            qid = str(item.get('_id'))
            product = Product.query.filter_by(qid=qid).first()
            price = float(item.get('price', 0))

            if not product:
                new_product = Product(qid=qid, title=item.get('title'), supplier_id=1, sku=item.get('sku'), cost_price=price)
                db.session.add(new_product)
                count += 1
            else:
                product.title = item.get('title', product.title)
                product.cost_price = price
        
        db.session.commit()
        return jsonify({"status": "success", "message": f"تمت معالجة {len(products_data)} منتج، إضافة {count} جديد."})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

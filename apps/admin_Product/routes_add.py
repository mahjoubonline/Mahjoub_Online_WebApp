# coding: utf-8
# 📂 apps/admin_Product/routes_add.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

@admin_product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        # تجهيز بيانات المنتج الجديد
        product_data = {
            "title": request.form.get('title'),
            "pricing": {"price": float(request.form.get('price', 0))},
            "quantity": int(request.form.get('quantity', 0))
        }

        mutation = """
        mutation Create($input: CreateProductInput!) {
            createProduct(input: $input) { qid }
        }
        """
        
        try:
            response = QomrahGraphQLClient.execute_query(mutation, {"input": product_data})
            if response and 'data' in response:
                flash("✅ تم إضافة المنتج بنجاح.")
                return redirect(url_for('admin_product_bp.manage_products'))
            else:
                flash("❌ فشل في إضافة المنتج.")
        except Exception as e:
            logger.error(f"خطأ أثناء الإضافة: {e}")
            flash("حدث خطأ تقني.")

    return render_template('admin/add_product.html')

# coding: utf-8
# 📂 apps/admin_Product/routes_edit.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from .registry import admin_product_bp
from apps.services.graphql_client import QomrahGraphQLClient
import logging

logger = logging.getLogger(__name__)

# استخدام <path:qid> يسمح بمرور المعرف الذي يحتوي على سلاشات (/) دون التسبب في خطأ 404
@admin_product_bp.route('/edit/<path:qid>', methods=['GET', 'POST'])
@login_required
def edit_product(qid):
    """تعديل بيانات المنتج لحظياً عبر API قمرة"""
    
    # 1. جلب تفاصيل المنتج الحالية
    if request.method == 'GET':
        query = """
        query Get($qid: ID!) { 
            findProduct(qid: $qid) { 
                title, pricing { price }, quantity 
            } 
        }
        """
        response = QomrahGraphQLClient.execute_query(query, {"qid": qid})
        
        # التأكد من صحة الاستجابة قبل تمريرها للقالب
        product = {}
        if response and 'data' in response and response['data'].get('findProduct'):
            product = response['data']['findProduct']
        else:
            flash("❌ تعذر جلب بيانات المنتج، قد يكون الرابط غير صالح.")
            return redirect(url_for('admin_product_bp.manage_products'))
            
        return render_template('admin/edit_product.html', product=product, qid=qid)

    # 2. تحديث المنتج (POST)
    if request.method == 'POST':
        update_data = {
            "title": request.form.get('title'),
            "pricing": {"price": float(request.form.get('price', 0))},
            "quantity": int(request.form.get('quantity', 0))
        }
        
        mutation = """
        mutation Update($qid: ID!, $input: UpdateProductInput!) { 
            updateProduct(qid: $qid, input: $input) { qid } 
        }
        """
        response = QomrahGraphQLClient.execute_query(mutation, {"qid": qid, "input": update_data})
        
        if response and 'data' in response:
            flash("✅ تم تحديث المنتج بنجاح.")
            return redirect(url_for('admin_product_bp.manage_products'))
        
        flash("❌ فشل تحديث المنتج في قمرة.")
        return redirect(url_for('admin_product_bp.edit_product', qid=qid))

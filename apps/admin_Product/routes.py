# coding: utf-8
# 📂 apps/admin_Product/routes.py

import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required
from apps.services.product_sync_service import fetch_products_from_qomra

logger = logging.getLogger(__name__)

admin_product_bp = Blueprint(
    'admin_product_bp', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

@admin_product_bp.route('/products', methods=['GET'])
@login_required
def manage_products():
    """
    جلب وعرض المنتجات مباشرة من قمرة لحظياً دون تخزين محلي.
    """
    search_query = request.args.get('title', '').strip()
    
    try:
        # جلب المنتجات مباشرة من خدمة قمرة
        products, pagination = fetch_products_from_qomra(search=search_query)
    except Exception as e:
        logger.error(f"Error fetching products from Qomra: {str(e)}", exc_info=True)
        products = []
        pagination = {'currentPage': 1, 'totalPages': 1, 'totalItems': 0}
        flash('حدث خطأ أثناء الاتصال بقمرة وجلب المنتجات.', 'danger')

    # إذا كان الطلب قادماً عبر AJAX للبحث الفوري
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template(
            'admin/includes/_table_products.html', 
            products=products, 
            pagination=pagination, 
            search=search_query
        )
        
    return render_template(
        'admin/admin_Product.html', 
        products=products, 
        pagination=pagination, 
        search=search_query
    )

# coding: utf-8
# 📂 apps/admin_Product/routes.py

import logging
from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from apps.services.product_sync_service import fetch_products_from_qomra

# إعداد السجلات للمراقبة
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
    جلب وعرض المنتجات مباشرة من قمرة لحظياً دون تخزين محلي، مع حماية ضد الأخطاء.
    """
    search_query = request.args.get('title', '').strip()
    
    products = []
    pagination = {'currentPage': 1, 'totalPages': 1, 'totalItems': 0}

    try:
        # جلب المنتجات مباشرة من خدمة قمرة
        fetched_products, fetched_pagination = fetch_products_from_qomra(search=search_query)
        if fetched_products is not None:
            products = fetched_products
        if fetched_pagination is not None:
            pagination = fetched_pagination
    except Exception as e:
        logger.error(f"Error fetching products from Qomra: {str(e)}", exc_info=True)
        flash('تعذر الاتصال بخادم قمرة لعرض المنتجات حالياً.', 'warning')

    # إذا كان الطلب قادماً عبر AJAX للبحث الفوري، يتم إرجاع الجدول الجزئي فقط
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


@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    """
    مسار فارغ لتوافق الواجهة (حيث أن النظام أصبح يعرض البيانات مباشرة من قمرة دون تخزين محلي).
    """
    return {
        'status': 'success',
        'message': 'النظام يعرض أحدث البيانات مباشرة من قمرة لحظياً.'
    }, 200

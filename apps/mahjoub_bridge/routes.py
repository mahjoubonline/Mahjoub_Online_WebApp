# 📂 apps/mahjoub_bridge/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.utils.products_engine import ProductsEngine
from flask_login import login_required
import logging

logger = logging.getLogger(__name__)
products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/products/sync', methods=['POST'])
@login_required
def sync_products():
    """مزامنة المنتجات من قمرة إلى قاعدة البيانات"""
    try:
        engine = ProductsEngine()
        count = engine.sync_products_to_db()
        return jsonify({'success': True, 'message': f'تمت مزامنة {count} منتج بنجاح.'})
    except Exception as e:
        logger.error(f"Error syncing products: {str(e)}")
        return jsonify({'success': False, 'message': 'فشل مزامنة المنتجات'}), 500

@products_bp.route('/products/list', methods=['GET'])
@login_required
def list_products():
    """عرض قائمة المنتجات"""
    search = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    engine = ProductsEngine()
    products = engine.fetch_all(search_term=search, page=page)
    return render_template('products/list.html', products=products)

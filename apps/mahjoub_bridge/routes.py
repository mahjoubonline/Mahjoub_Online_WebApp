# coding: utf-8
# 📂 apps/mahjoub_bridge/routes.py

from flask import Blueprint, render_template, request, jsonify
from apps.utils.bridge_engine import QumraBridgeEngine
import traceback

bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/dashboard', methods=['GET'])
def dashboard():
    search = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    engine = QumraBridgeEngine()
    products = engine.fetch_products(search_term=search, page=page)
    
    return render_template('admin/bridge_dashboard.html', 
                           products=products, 
                           search=search,
                           page=page)

@bridge_bp.route('/sync-now', methods=['POST'])
def sync_now():
    """المزامنة اللحظية (تستخدم نفس محرك البحث)."""
    try:
        engine = QumraBridgeEngine()
        products = engine.fetch_products(search_term="", page=1)
        
        if not products:
            return jsonify({"status": "error", "message": "لم يتم العثور على منتجات في الاستجابة"})

        return jsonify({
            "status": "success", 
            "message": f"تم جلب {len(products)} منتج بنجاح"
        })
        
    except Exception:
        return jsonify({"status": "error", "message": "خطأ في الاتصال بالمحرك"}), 500

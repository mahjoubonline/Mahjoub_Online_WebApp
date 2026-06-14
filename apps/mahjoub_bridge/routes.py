# 📂 apps/mahjoub_bridge/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.utils.bridge_engine import QumraBridgeEngine

bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/bridge/dashboard', methods=['GET'])
def dashboard():
    search = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    engine = QumraBridgeEngine()
    data = engine.fetch_products(search_term=search, page=page, per_page=per_page)
    return render_template('admin/bridge_dashboard.html', data=data, search=search)

@bridge_bp.route('/bridge/api/search', methods=['GET'])
def api_search():
    search = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    engine = QumraBridgeEngine()
    return jsonify(engine.fetch_products(search_term=search, page=page, per_page=per_page))

@bridge_bp.route('/bridge/sync-now', methods=['POST'])
def sync_now():
    engine = QumraBridgeEngine()
    if engine.sync_all_data():
        return jsonify({"status": "success", "message": "تم التحديث"})
    return jsonify({"status": "error", "message": "فشل الاتصال"}), 500

# 📂 apps/mahjoub_bridge/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.utils.bridge_engine import QumraBridgeEngine

bridge_bp = Blueprint('mahjoub_bridge', __name__)

@bridge_bp.route('/dashboard')
def dashboard():
    return render_template('admin/bridge_dashboard.html')

@bridge_bp.route('/api/search')
def api_search():
    engine = QumraBridgeEngine()
    query = request.args.get('q', '')
    return jsonify({"products": engine.get_data(query)})

@bridge_bp.route('/sync', methods=['POST'])
def sync():
    engine = QumraBridgeEngine()
    return jsonify({"status": "success" if engine.sync_all_data() else "error"})

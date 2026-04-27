from flask import render_template, request, jsonify
from flask_login import login_required
from . import admin_bp
from services.qumra_handler import query_qumra # لاستخدام محرك GraphQL

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin_panel/dashboard.html')

# استقبال إشارات قمرة (Webhook) الذي ربطته في الصورة السابقة
@admin_bp.route('/api/qumra/webhook/', methods=['POST'])
def qumra_webhook():
    data = request.json
    # معالجة بيانات الطلب القادم من قمرة
    print(f"📦 طلب جديد من قمرة: {data}")
    return jsonify({"status": "success"}), 200

# مثال لاستخدام GraphQL لجلب البيانات
@admin_bp.route('/sync-collections')
@login_required
def sync_collections():
    query = "{ collections(first: 10) { edges { node { name } } } }"
    result = query_qumra(query)
    return jsonify(result)

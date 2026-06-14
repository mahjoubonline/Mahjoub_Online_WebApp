# 📂 apps/mahjoub_bridge/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.utils.bridge_engine import QumraBridgeEngine

bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """عرض لوحة التحكم الخاصة بالجسر"""
    return render_template('admin/bridge_dashboard.html')

@bridge_bp.route('/api/search', methods=['GET'])
def api_search():
    """
    نقطة اتصال للبحث المباشر. تستقبل النص، وتجلب البيانات، وتعيدها كـ JSON.
    """
    search_query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    
    # استدعاء المحرك المطور
    engine = QumraBridgeEngine()
    data = engine.fetch_products_from_qumra(search_query, page)
    
    # إرجاع البيانات بتنسيق متوافق تماماً مع الواجهة
    return jsonify({
        "status": "success",
        "products": data,
        "count": len(data)
    })

@bridge_bp.route('/sync', methods=['POST'])
def sync():
    """تشغيل عملية المزامنة يدوياً"""
    engine = QumraBridgeEngine()
    # تأكد من أن sync_all_data موجودة في Engine أو استبدلها بالدالة الصحيحة
    success = engine.sync_all_data() if hasattr(engine, 'sync_all_data') else False
    return jsonify({"status": "success" if success else "error"})

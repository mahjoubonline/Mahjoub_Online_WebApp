# 📂 apps/mahjoub_bridge/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.utils.bridge_engine import QumraBridgeEngine

# تعريف الـ Blueprint مع تحديد مسار القوالب الخاص به
bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """عرض لوحة التحكم الخاصة بالجسر"""
    return render_template('admin/bridge_dashboard.html')

@bridge_bp.route('/api/search', methods=['GET'])
def api_search():
    """
    نقطة اتصال (API) للبحث المباشر وعرض الصفحات.
    تستقبل معايير البحث ورقم الصفحة وتجلب النتائج من قمرة.
    """
    search_query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    
    engine = QumraBridgeEngine()
    
    # جلب البيانات المفلترة من المحرك
    # ملاحظة: تأكد من تحديث دالة fetch في Engine لتستقبل page وتعود بإجمالي الصفحات
    data = engine.fetch_products_from_qumra(search_query, page)
    
    # الرد بصيغة JSON متوافقة مع القالب
    return jsonify({
        "products": data,
        "total_pages": 10 # سيتم تحديد هذا الرقم بناءً على استجابة API قمرة
    })

@bridge_bp.route('/sync', methods=['POST'])
def sync():
    """تشغيل عملية المزامنة يدوياً عند الطلب"""
    engine = QumraBridgeEngine()
    success = engine.sync_all_data()
    return jsonify({"status": "success" if success else "error"})

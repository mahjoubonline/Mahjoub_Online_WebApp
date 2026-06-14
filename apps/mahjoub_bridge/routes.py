# coding: utf-8
# 📂 apps/mahjoub_bridge/routes.py

from flask import Blueprint, render_template, request, jsonify
from apps.utils.bridge_engine import QumraBridgeEngine
import traceback

bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    لوحة التحكم:
    تعتمد على المحرك لجلب البيانات، والترقيم، والبحث.
    يتم تمرير القاموس 'data' الذي يحتوي على المنتجات ومعلومات الترقيم.
    """
    search = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    
    # استدعاء المحرك
    engine = QumraBridgeEngine()
    
    # المحرك الآن يرجع قاموساً (dictionary) يحتوي على {products, total, page, total_pages}
    # بفضل منطق الترقيم الذي أضفناه للمحرك
    data = engine.fetch_products(search_term=search, page=page)
    
    return render_template('admin/bridge_dashboard.html', 
                           data=data, 
                           search=search)

@bridge_bp.route('/sync-now', methods=['POST'])
def sync_now():
    """
    المزامنة:
    تقوم بتحديث الذاكرة المؤقتة (Cache) مباشرة من النظام السيادي.
    """
    try:
        engine = QumraBridgeEngine()
        # نستخدم دالة التحديث القسري الموجودة في المحرك
        success = engine.sync_all_data()
        
        if success:
            return jsonify({
                "status": "success", 
                "message": "تم تحديث البيانات بالكامل من النظام السيادي"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "فشل الاتصال بالنظام السيادي - تأكد من صلاحية الـ API Key"
            }), 500
        
    except Exception:
        print(f"❌ Sync Error: {traceback.format_exc()}")
        return jsonify({
            "status": "error", 
            "message": "حدث خطأ غير متوقع أثناء المزامنة"
        }), 500

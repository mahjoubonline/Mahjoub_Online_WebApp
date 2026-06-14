# coding: utf-8
# 📂 apps/mahjoub_bridge/routes.py

from flask import Blueprint, render_template, request, jsonify
from apps.utils.bridge_engine import QumraBridgeEngine
import traceback

bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """لوحة تحكم تعتمد على البحث المباشر في الذاكرة المؤقتة."""
    search = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    
    # استدعاء المحرك الذي سيستخدم الـ Cache تلقائياً
    engine = QumraBridgeEngine()
    products = engine.fetch_products(search_term=search, page=page)
    
    return render_template('admin/bridge_dashboard.html', 
                           products=products, 
                           search=search,
                           page=page)

@bridge_bp.route('/sync-now', methods=['POST'])
def sync_now():
    """تحديث قسري للبيانات من قمرة (تحديث الـ Cache)."""
    try:
        engine = QumraBridgeEngine()
        # نستخدم دالة التحديث القسري التي أنشأناها في المحرك
        success = engine.sync_all_data()
        
        if success:
            return jsonify({
                "status": "success", 
                "message": "تم تحديث البيانات بالكامل من النظام السيادي"
            })
        else:
            return jsonify({"status": "error", "message": "فشل الاتصال بالنظام السيادي"}), 500
        
    except Exception:
        print(f"❌ Sync Error: {traceback.format_exc()}")
        return jsonify({"status": "error", "message": "حدث خطأ غير متوقع أثناء المزامنة"}), 500

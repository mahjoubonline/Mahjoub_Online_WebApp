# coding: utf-8
# 📂 apps/mahjoub_bridge/routes.py

from flask import Blueprint, render_template, request, jsonify
from apps.utils.bridge_engine import QumraBridgeEngine
import traceback

bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """لوحة تحكم تعتمد على البحث المباشر في قمرة."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '', type=str)
    
    # استخدام المحرك الجديد للبحث المباشر
    engine = QumraBridgeEngine()
    
    # جلب المنتجات مباشرة من قمرة بناءً على نص البحث ورقم الصفحة
    products = engine.fetch_products(search_term=search, page=page)
    
    # ملاحظة: في هذه الحالة، الـ pagination يعتمد على ما يرجعه المحرك
    return render_template('admin/bridge_dashboard.html', 
                           products=products, 
                           search=search,
                           page=page)

@bridge_bp.route('/sync-now', methods=['POST'])
def sync_now():
    """هذا المسار يظل كما هو إذا كنت تريد تخزين بعض المنتجات محلياً عند الحاجة."""
    try:
        engine = QumraBridgeEngine()
        products = engine.fetch_products(search_term="", page=1) # جلب الصفحة الأولى للتمثيل
        
        if not products:
            return jsonify({"status": "error", "message": "لم يتم العثور على منتجات"})

        # هنا يمكنك إضافة منطق التخزين المحلي إذا رغبت في ذلك لاحقاً
        return jsonify({"status": "success", "message": f"تم استلام {len(products)} منتج من المحرك بنجاح"})
        
    except Exception:
        print(f"❌ Error in sync: {traceback.format_exc()}")
        return jsonify({"status": "error", "message": "حدث خطأ أثناء الاتصال بالمحرك"}), 500

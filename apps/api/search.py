# 📂 apps/api/search.py - الملف الكامل والمكتمل
from flask import Blueprint, request, jsonify
from flask_login import login_required
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint
api_search = Blueprint('api_search', __name__)

# هذا المسار سيكون: /api/search
@api_search.route('/search', methods=['GET'])
@login_required
def search_suppliers():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"results": []})

    # المحرك يبحث في الحقول المفهرسة
    suppliers = Supplier.query.filter(
        (Supplier.search_name.ilike(f'%{query}%')) | 
        (Supplier.search_phone.ilike(f'%{query}%'))
    ).limit(10).all()

    # تجهيز النتائج بتنسيق id و text ليقرأها Select2 مباشرة
    results = [
        {"id": s.id, "text": f"{s.trade_name} - {s.owner_phone}"} 
        for s in suppliers
    ]
    return jsonify({"results": results})

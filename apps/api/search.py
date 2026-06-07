# coding: utf-8
# 📂 apps/api/search.py - محرك البحث الاحترافي للموردين

from flask import Blueprint, request, jsonify
from flask_login import login_required
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint باسم api_search
api_search = Blueprint('api_search', __name__)

# هذا المسار سيكون: /api/search
@api_search.route('/search', methods=['GET'])
@login_required # حماية المسار لضمان أن المستخدم مسجل دخول
def search_suppliers():
    query = request.args.get('q', '').strip()
    
    # في حالة عدم وجود استعلام، إرجاع قائمة فارغة
    if not query:
        return jsonify({"results": []})

    # البحث باستخدام الحقول المفهرسة (search_name, search_phone)
    # ilike تجعل البحث غير حساس لحالة الأحرف
    suppliers = Supplier.query.filter(
        (Supplier.search_name.ilike(f'%{query}%')) | 
        (Supplier.search_phone.ilike(f'%{query}%'))
    ).limit(10).all()

    # تنسيق النتائج (مع الاعتماد على خصائص فك التشفير في الموديل)
    results = [
        {
            "id": s.id,
            "name": s.trade_name,  # يقوم بفك تشفير الاسم تلقائياً
            "phone": s.owner_phone # يقوم بفك تشفير الهاتف تلقائياً
        } for s in suppliers
    ]

    return jsonify({"results": results})

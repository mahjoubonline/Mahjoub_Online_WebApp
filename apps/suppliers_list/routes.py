# coding: utf-8
# 📂 apps/suppliers_list/routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy.orm import joinedload
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint الخاص بموديول الشركاء
supplier_bp = Blueprint(
    'supplier_app', 
    __name__, 
    template_folder='templates'
)

@supplier_bp.route('/list', methods=['GET'])
@login_required
def list_suppliers():
    """
    عرض قائمة الشركاء مع دعم البحث والترقيم (Pagination).
    يتم جلب البيانات المرتبطة (Profile & Staff) بكفاءة عالية.
    """
    # 1. استقبال بارامترات البحث والصفحة
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    
    # 2. بناء الاستعلام الأساسي مع تحميل استباقي للعلاقات
    query = Supplier.query.options(
        joinedload(Supplier.supplier_profile),
        joinedload(Supplier.staff_members)
    )
    
    # 3. تطبيق فلتر البحث في حال وجود نص
    if search_query:
        query = query.filter(
            (Supplier.trade_name.ilike(f'%{search_query}%')) | 
            (Supplier.supplier_code.ilike(f'%{search_query}%'))
        )
        
    # 4. الترتيب والترقيم (20 عنصراً في كل صفحة)
    pagination = query.order_by(Supplier.created_at.desc()).paginate(
        page=page, 
        per_page=20, 
        error_out=False
    )
    
    return render_template(
        'suppliers_list/suppliers_list.html', 
        suppliers=pagination.items,
        pagination=pagination,
        search=search_query
    )

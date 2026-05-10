# admin_panel/add_supplier_routes.py
from flask import render_template, request, jsonify
from flask_login import login_required
from . import admin_bp
from .engines.supplier_engine import create_new_supplier  # استدعاء المحرك السيادي
from core.models.supplier import Supplier # استيراد الموديل للبحث والجلب
from app import db # لضمان الوصول لقاعدة البيانات عند الحاجة للبحث المعقد

@admin_bp.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """مسار التعميد السيادي للموردين"""
    if request.method == 'POST':
        # نرسل البيانات للمحرك وننتظر النتيجة
        success, result = create_new_supplier(request.form)
        
        if success:
            return jsonify({
                "status": "success", 
                "message": f"تم التعميد بنجاح! المعرف السيادي: {result}"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": f"فشل التعميد: {result}"
            }), 500

    # في حالة GET: عرض صفحة الإضافة مع حساب المعرف التالي
    last_s = Supplier.query.order_by(Supplier.id.desc()).first()
    next_id = (last_s.id + 1) if last_s else 1
    return render_template('admin/add_supplier.html', next_id=next_id)

@admin_bp.route('/api/suppliers/search', methods=['GET'])
@login_required
def search_suppliers_api():
    """محرك الاستدعاء الذكي: يخدم واجهة manage_suppliers"""
    query_text = request.args.get('q', '').strip()
    province = request.args.get('province', '')
    status = request.args.get('status', '')

    # بناء الاستعلام الأساسي مرتباً حسب الأحدث (السيادة للأحدث دائماً)
    base_query = Supplier.query.order_by(Supplier.id.desc())

    # منطق الفلترة الذكية
    if query_text:
        # إذا أدخل المستخدم # نجلب الكل، وإلا نبحث في الحقول الأساسية
        if query_text != "#":
            search_pattern = f"%{query_text}%"
            base_query = base_query.filter(
                (Supplier.trade_name.like(search_pattern)) |
                (Supplier.owner_name.like(search_pattern)) |
                (Supplier.phone.like(search_pattern)) |
                (Supplier.sovereign_id.like(search_pattern))
            )
    
    if province:
        base_query = base_query.filter(Supplier.province == province)
    
    if status:
        base_query = base_query.filter(Supplier.status == status)

    # القاعدة الذهبية: إذا لم يوجد بحث، جلب آخر 10 فقط. إذا وجد بحث، جلب النتائج.
    if not (query_text or province or status):
        suppliers = base_query.limit(10).all()
    else:
        suppliers = base_query.all()

    # تحويل الكيانات البرمجية إلى تنسيق JSON لترجمته في الواجهة
    output = []
    for s in suppliers:
        output.append({
            "id": s.id,
            "sovereign_id": s.sovereign_id,
            "trade_name": s.trade_name,
            "owner_name": s.owner_name,
            "province": s.province,
            "tier": s.tier or "مبتدئ",
            "balance_yer": s.balance_yer or 0,
            "balance_sar": s.balance_sar or 0,
            "balance_usd": s.balance_usd or 0,
            "status": s.status,
            "staff_count": getattr(s, 'staff_count', 0) # التأكد من عدم الخطأ إذا لم يوجد الحقل
        })

    return jsonify(output)

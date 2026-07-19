# مسار الملف: apps/admin_Product/routes_sync.py

from flask import request, jsonify
from models import db, Product, Variant, Collection

@admin_product_bp.route('/save-sync', methods=['POST'])
def save_sync():
    data = request.json
    qid = data.get('qid')
    
    # 1. البحث عن المنتج في قاعدة البيانات
    product = Product.query.filter_by(qid=qid).first()
    if not product:
        return jsonify({"status": "error", "message": "المنتج غير موجود"}), 404
    
    # 2. تحديث البيانات الأساسية
    product.title = data.get('title')
    product.slug = data.get('slug')
    product.description = data.get('description')
    product.supplier_id = data.get('supplier_id')
    
    # 3. تحديث المجموعات (Collections)
    product.collections = Collection.query.filter(Collection.qid.in_(data.get('collection_ids', []))).all()
    
    # 4. تحديث المتغيرات (Variants)
    # حذف المتغيرات القديمة وإعادة إنشاء الجديدة بناءً على القائمة المرسلة
    Variant.query.filter_by(product_id=product.id).delete()
    for v_data in data.get('variants', []):
        new_variant = Variant(
            product_id=product.id,
            title=v_data['title'],
            price=v_data['price'],
            quantity=v_data['quantity'],
            sku=v_data['sku']
        )
        db.session.add(new_variant)
        
    db.session.commit()
    return jsonify({"status": "success", "message": "تم الحفظ بنجاح"})

# 📂 apps/admin_Product/routes_sync.py

# تأكد من استيراد النماذج الصحيحة
from apps.models.product_db import Product  # مثال لمسار نموذج المنتج
from apps.models.product_supplier_map import ProductSupplierMapping
from models import db

@admin_product_bp.route('/save-sync', methods=['POST'])
def save_sync():
    data = request.json
    qid = data.get('qid')
    
    # تحديث المورد في جدول الربط (ProductSupplierMapping)
    mapping = ProductSupplierMapping.query.filter_by(product_qid=qid).first()
    if mapping:
        mapping.supplier_id = data.get('supplier_id')
    else:
        new_mapping = ProductSupplierMapping(product_qid=qid, supplier_id=data.get('supplier_id'))
        db.session.add(new_mapping)
        
    # ثم تابع تحديث البيانات الأساسية والمتغيرات في قاعدة بياناتك المحلية كما في الكود السابق
    # ...
    db.session.commit()
    return jsonify({"status": "success"})

# 📂 apps/admin_Product/routes_sync.py

from flask import request, jsonify
from .registry import admin_product_bp
from apps.models.product_supplier_map import ProductSupplierMapping
from models import db
import logging

logger = logging.getLogger(__name__)

@admin_product_bp.route('/save-sync', methods=['POST'])
def save_sync():
    data = request.json
    qid = data.get('qid')
    
    if not qid:
        return jsonify({"status": "error", "message": "QID مفقود"}), 400

    try:
        # 1. تحديث المورد في جدول الربط
        mapping = ProductSupplierMapping.query.filter_by(product_qid=qid).first()
        if mapping:
            mapping.supplier_id = data.get('supplier_id')
        else:
            new_mapping = ProductSupplierMapping(product_qid=qid, supplier_id=data.get('supplier_id'))
            db.session.add(new_mapping)
            
        # 2. ملاحظة: إذا كان لديك نموذج محلي للمنتج لتخزين المتغيرات أو السعر
        # يمكنك إضافته هنا. مثال:
        # product = Product.query.filter_by(qid=qid).first()
        # if product:
        #     product.title = data.get('title')
        #     product.description = data.get('description')
        #     # تحديث المتغيرات أو المجموعات...

        db.session.commit()
        return jsonify({"status": "success", "message": "تم تحديث البيانات بنجاح"})
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ أثناء الحفظ: {str(e)}")
        return jsonify({"status": "error", "message": "فشل الاتصال بقاعدة البيانات"}), 500

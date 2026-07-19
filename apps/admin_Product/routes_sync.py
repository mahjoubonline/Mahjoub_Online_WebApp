# coding: utf-8
# 📂 apps/admin_Product/routes_sync.py

from flask import request, jsonify
from .registry import admin_product_bp
import logging

# بما أننا لا نستخدم قاعدة بيانات محلية للمنتجات، سنقوم بإزالة استيراداتها
# إذا كنت تحتاج حقاً لجدول Mapping، فتأكد أن المسار صحيح وموجود
try:
    from apps.models.product_supplier_map import ProductSupplierMapping
    from apps.extensions import db
    HAS_DB = True
except ImportError:
    HAS_DB = False
    logging.warning("⚠️ قاعدة بيانات الربط غير متاحة - تم تعطيل المزامنة المحلية.")

logger = logging.getLogger(__name__)

@admin_product_bp.route('/save-sync', methods=['POST'])
def save_sync():
    if not HAS_DB:
        return jsonify({"status": "error", "message": "قاعدة البيانات غير مهيأة"}), 500

    data = request.json
    qid = data.get('qid')
    supplier_id = data.get('supplier_id')
    
    if not qid:
        return jsonify({"status": "error", "message": "QID مفقود"}), 400

    try:
        # تحديث أو إضافة الربط بالمورد فقط
        mapping = ProductSupplierMapping.query.filter_by(product_qid=qid).first()
        if mapping:
            mapping.supplier_id = supplier_id
        else:
            new_mapping = ProductSupplierMapping(product_qid=qid, supplier_id=supplier_id)
            db.session.add(new_mapping)
            
        db.session.commit()
        return jsonify({"status": "success", "message": "تم حفظ بيانات الربط بنجاح"})
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ خطأ أثناء حفظ الربط: {str(e)}")
        return jsonify({"status": "error", "message": "فشل الحفظ"}), 500

# coding: utf-8
# 📂 apps/api/sync_engine.py

import logging
from apps.extensions import db
from apps.models.product_db import Product

logger = logging.getLogger(__name__)

class ProductSyncEngine:

    @staticmethod
    def process_products(products_data):
        if not products_data or not isinstance(products_data, list):
            logger.warning("❌ لم يتم استقبال بيانات صالحة للمزامنة.")
            return 0
            
        synced_count = 0
        for item in products_data:
            try:
                qid = str(item.get('qid'))
                product = Product.query.filter_by(qid=qid).first() or Product(qid=qid)
                
                # تحديث البيانات الأساسية
                product.title = item.get('title', 'منتج غير معرف')
                product.quantity = item.get('quantity', 0)
                
                # استخراج البيانات المتداخلة
                pricing = item.get('pricing', {}) or {}
                identification = item.get('identification', {}) or {}
                weight_info = item.get('weight', {}) or {}
                images = item.get('images', [])
                
                # السعر
                product.cost_price = float(pricing.get('price', 0))
                
                # SKU والوزن
                product.sku = identification.get('sku')
                product.weight_val = weight_info.get('weight')
                product.weight_unit = weight_info.get('unit')
                
                # الصور (أول صورة)
                if isinstance(images, list) and len(images) > 0:
                    product.image_url = images[0].get('fileUrl')

                db.session.add(product)
                synced_count += 1
            except Exception as e:
                logger.error(f"❌ خطأ في معالجة المنتج {item.get('qid', 'unknown')}: {e}")
                continue
        
        db.session.commit()
        return synced_count

# coding: utf-8
# 📂 apps/services/product_sync_service.py

from apps.extensions import db
from apps.models.product_db import Product
from apps.models.product_supplier_map import ProductSupplierMapping
from apps.services.graphql_client import QomrahGraphQLClient

def sync_products_from_qomra():
    """
    خدمة مزامنة المنتجات باستخدام الكلاينت المركزي الموحد QomrahGraphQLClient
    """
    query = """
    query {
        findAllProducts {
            id
            title
            price
            currency
            quantity
            sku
            image_url
            description
        }
    }
    """

    # استخدام الكلاينت المركزي المنظم لتنفيذ الاستعلام بأمان
    result = QomrahGraphQLClient.execute_query(query)
    
    if not result:
        raise Exception("فشل الاتصال بخادم قمرة أو تعذر جلب البيانات عبر GraphQL.")

    data = result.get('data', {})
    products_data = data.get('findAllProducts', [])

    if not products_data:
        return "تمت المزامنة بنجاح، لكن لم يتم العثور على منتجات لجلبها."

    synced_count = 0
    for item in products_data:
        qid = str(item.get('id') or item.get('qid') or '')
        if not qid:
            continue

        title = item.get('title') or item.get('name') or 'منتج بدون اسم'
        price = float(item.get('price') or 0)
        currency = item.get('currency') or 'SAR'
        quantity = int(item.get('quantity') or 0)
        sku = item.get('sku') or ''
        image_url = item.get('image_url') or item.get('image') or ''
        description = item.get('description') or ''

        product = Product.query.filter_by(qid=qid).first()
        if product:
            product.title = title
            product.price = price
            product.currency = currency
            product.quantity = quantity
            product.sku = sku
            product.image_url = image_url
            product.description = description
        else:
            product = Product(
                qid=qid, title=title, price=price, currency=currency,
                quantity=quantity, sku=sku, image_url=image_url, description=description
            )
            db.session.add(product)

            mapping = ProductSupplierMapping.query.filter_by(product_qid=qid).first()
            if not mapping:
                new_mapping = ProductSupplierMapping(product_qid=qid, supplier_id=1, status='active')
                db.session.add(new_mapping)

        synced_count += 1

    db.session.commit()
    return f"تمت مزامنة وتحديث {synced_count} منتجاً بنجاح من قمرة."

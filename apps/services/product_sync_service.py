# coding: utf-8
# 📂 apps/services/product_sync_service.py

import requests
from flask import current_app
from apps.extensions import db
from apps.models.product_db import Product
from apps.models.product_supplier_map import ProductSupplierMapping

def sync_products_from_qomra():
    """
    خدمة مزامنة المنتجات من قمرة عبر GraphQL مع تصحيح هيكل الاستعلام 
    ليطابق مخطط السيرفر الفعلي وتفادي أخطاء الـ Validation.
    """
    graphql_url = current_app.config.get('QOMRA_GRAPHQL_URL', 'https://api.qomra.cloud/graphql')
    api_token = current_app.config.get('QOMRA_API_TOKEN', '')

    # استعلام GraphQL مصحح يتوافق مع المخطط الفعلي (بدون arguments غير مدعومة)
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

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}" if api_token else ""
    }

    try:
        response = requests.post(graphql_url, json={'query': query}, headers=headers, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"خطأ في الاتصال بالسيرفر: رمز الاستجابة {response.status_code}")

        result = response.json()
        
        if "errors" in result:
            error_msgs = [err.get('message', 'خطأ غير معروف') for err in result['errors']]
            raise Exception(f"أخطاء GraphQL: {', '.join(error_msgs)}")

        data = result.get('data', {})
        products_data = data.get('findAllProducts', [])

        if not products_data:
            return "تمت المزامنة بنجاح، لكن لم يتم العثور على منتجات جديدة لجلبها."

        synced_count = 0
        for item in products_data:
            # استخراج المعرف الفريد (qid) مع دعم البدائل
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

            # البحث عن المنتج محلياً لتحديثه أو إضافته
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
                    qid=qid,
                    title=title,
                    price=price,
                    currency=currency,
                    quantity=quantity,
                    sku=sku,
                    image_url=image_url,
                    description=description
                )
                db.session.add(product)

                # إضافة جدول الربط للمورد إذا لم يكن موجوداً
                mapping = ProductSupplierMapping.query.filter_by(product_qid=qid).first()
                if not mapping:
                    new_mapping = ProductSupplierMapping(
                        product_qid=qid,
                        supplier_id=1,
                        status='active'
                    )
                    db.session.add(new_mapping)

            synced_count += 1

        db.session.commit()
        return f"تمت مزامنة وتحديث {synced_count} منتجاً بنجاح من قمرة."

    except Exception as e:
        db.session.rollback()
        raise e

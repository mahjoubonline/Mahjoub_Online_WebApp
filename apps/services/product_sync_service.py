# coding: utf-8
# 📂 apps/services/product_sync_service.py

import uuid
import logging
from apps.extensions import db
from apps.models.product_db import Product
from apps.models.product_supplier_map import ProductSupplierMapping
from apps.services.graphql_client import QomrahGraphQLClient

def sync_products_from_qomra():
    """
    جلب المنتجات ديناميكياً وبشكل تصاعدي (Pagination Loop) من منصة قمرة 
    لضمان استيعاب أي عدد متزايد من المنتجات لحظياً دون فقدان أي بيانات،
    مع معالجة متقدمة للأسعار والصور والربط السيادي.
    """
    all_products_collected = []
    page = 1
    limit = 50  # حجم الدفعة لكل طلب لضمان السرعة وتجاوز حدود الـ Timeouts
    max_safety_pages = 100  # حماية لمنع الحلقات اللانهائية

    while page <= max_safety_pages:
        # استعلام ديناميكي يدعم الترقيم الصفحي لجلب كل المنتجات المتزايدة باستمرار
        query = f"""
        query GetAllProductsUnified {{
            findAllProducts(page: {page}, limit: {limit}) {{
                items {{
                    qid
                    id
                    title
                    name
                    description
                    quantity
                    price
                    salePrice
                    images {{
                        _id
                        fileUrl
                        url
                        path
                    }}
                    pricing {{
                        price
                        originalPrice
                        salePrice
                        amount
                        regularPrice
                    }}
                }}
                totalPages
                totalItems
                hasNextPage
            }}
        }}
        """
        
        try:
            result = QomrahGraphQLClient.execute_query(query)
        except Exception as e:
            logging.error(f"❌ خطأ أثناء تنفيذ استعلام المزامنة للصفحة {page}: {e}")
            # في حال لم يدعم السيرفر معاملات الترقيم، نحاول استعلاماً مبسطاً لمرة واحدة كاحتياط
            if page == 1:
                fallback_query = """
                query GetAllProductsUnifiedFallback {
                    findAllProducts {
                        items {
                            qid
                            id
                            title
                            name
                            description
                            quantity
                            price
                            salePrice
                            images {
                                _id
                                fileUrl
                                url
                                path
                            }
                            pricing {
                                price
                                originalPrice
                                salePrice
                                amount
                                regularPrice
                            }
                        }
                    }
                }
                """
                try:
                    result = QomrahGraphQLClient.execute_query(fallback_query)
                except Exception as ex:
                    raise Exception(f"فشل الاتصال بخدمة قمرة: {str(ex)}")
            else:
                break

        if not result:
            break

        response_data = result.get('data', result)
        page_items = []

        if isinstance(response_data, dict):
            find_all = response_data.get('findAllProducts') or response_data.get('data') or response_data
            if isinstance(find_all, dict):
                page_items = (
                    find_all.get('items') or 
                    find_all.get('data') or 
                    find_all.get('results') or 
                    find_all.get('products') or []
                )
            elif isinstance(find_all, list):
                page_items = find_all
        elif isinstance(response_data, list):
            page_items = response_data

        if not page_items:
            break  # توقف الحلقة عندما لا تعود المنصة بأي منتجات إضافية

        all_products_collected.extend(page_items)
        logging.info(f"📦 [Qomra Sync] Fetched page {page}, items count: {len(page_items)}, total so far: {len(all_products_collected)}")

        # إذا كان عدد المنتجات في الدفعة أقل من الحد الأقصى، فهذا يعني أننا وصلنا لنهاية المنتجات
        if len(page_items) < limit:
            break

        # التحقق من مؤشرات الترقيم إن وجدت لإيقاف الحلقة مبكراً
        if page == 1 and isinstance(response_data, dict):
            find_all_obj = response_data.get('findAllProducts')
            if isinstance(find_all_obj, dict) and not find_all_obj.get('hasNextPage') and 'totalPages' not in find_all_obj:
                break

        page += 1

    if not all_products_collected:
        return "تمت المزامنة بنجاح، لكن منصة قمرة لم تقم بإرجاع أي منتجات."

    logging.info(f"🚀 [Total Parsed Products from Qomra (Dynamic)]: {len(all_products_collected)}")

    saved_count = 0
    updated_count = 0
    mappings_count = 0

    default_supplier_id = 1
    try:
        from apps.models.supplier_db import Supplier
        first_supplier = Supplier.query.first()
        if first_supplier:
            default_supplier_id = first_supplier.id
    except Exception:
        pass

    for item in all_products_collected:
        if not isinstance(item, dict):
            continue
            
        title = item.get('title') or item.get('name')
        if not title:
            continue
            
        qid = item.get('qid') or item.get('_id') or item.get('id')
        description = item.get('description', '')
        
        try:
            quantity = int(item.get('quantity', 0) or 0)
        except (ValueError, TypeError):
            quantity = 0
        
        # استخراج الصورة بدقة عالية مع دعم كافة الاحتمالات
        images = item.get('images', [])
        image_url = None
        if images and isinstance(images, list):
            first_img = images[0]
            if isinstance(first_img, dict):
                image_url = first_img.get('fileUrl') or first_img.get('url') or first_img.get('path')
            elif isinstance(first_img, str):
                image_url = first_img
        
        # استخراج السعر والعملة بمرونة فائقة لمنع ظهور القيمة صفر
        price_val = 0
        currency = 'SAR'
        
        pricing = item.get('pricing')
        if isinstance(pricing, dict):
            price_val = (
                pricing.get('price') or 
                pricing.get('salePrice') or 
                pricing.get('originalPrice') or 
                pricing.get('amount') or 
                pricing.get('regularPrice') or 0
            )
        elif isinstance(pricing, (int, float, str)):
            price_val = pricing

        if not price_val or float(str(price_val) or 0) == 0:
            price_val = (
                item.get('price') or 
                item.get('salePrice') or 
                item.get('originalPrice') or 
                item.get('regularPrice') or 0
            )

        try:
            if isinstance(price_val, str):
                cleaned = ''.join(c for c in price_val if c.isdigit() or c == '.')
                price = float(cleaned) if cleaned else 0.0
            else:
                price = float(price_val or 0.0)
        except (ValueError, TypeError):
            price = 0.0

        product_qid_str = str(qid) if qid else f"qomra_{uuid.uuid4().hex[:8]}"

        # حفظ أو تحديث المنتج في جدول المنتجات المحلي
        product = None
        if qid:
            product = Product.query.filter_by(qid=str(qid)).first()
        if not product:
            product = Product.query.filter_by(title=title).first()
            
        if product:
            product.qid = product_qid_str
            product.title = title
            product.price = price
            product.currency = currency
            product.quantity = quantity
            if image_url:
                product.image_url = image_url
            product.description = description
            updated_count += 1
        else:
            new_product = Product(
                qid=product_qid_str,
                title=title,
                price=price,
                currency=currency,
                quantity=quantity,
                image_url=image_url,
                description=description
            )
            db.session.add(new_product)
            saved_count += 1

        # ضمان وجود سجل ربط سيادي في جدول ProductSupplierMapping
        if product_qid_str:
            mapping = ProductSupplierMapping.query.filter_by(product_qid=product_qid_str).first()
            if not mapping:
                new_mapping = ProductSupplierMapping(
                    product_qid=product_qid_str,
                    supplier_id=default_supplier_id,
                    status='active'
                )
                db.session.add(new_mapping)
                mappings_count += 1
                
    db.session.commit()
    
    return f"تمت المزامنة بنجاح! تم جلب ومعالجة {len(all_products_collected)} منتج ديناميكياً: إضافة {saved_count}، تحديث {updated_count}، وربط {mappings_count} منتج."

# coding: utf-8
# 📂 apps/services/product_sync_service.py

import os
import requests
import logging

logger = logging.getLogger(__name__)

QOMRA_GRAPHQL_URL = os.getenv("QOMRA_GRAPHQL_URL", "https://api.qumra.cloud/graphql")
QOMRA_API_TOKEN = os.getenv("QOMRA_API_TOKEN", "")

# ✅ الاستعلام المحدث المتوافق مع هيكل الصور الصحيح images { _id fileUrl }
PRODUCTS_QUERY = """
query FetchAllProducts {
    findAllProducts {
        success
        message
        data {
            id
            title
            description
            sku
            quantity
            pricing {
                price
            }
            images {
                _id
                fileUrl
            }
        }
        pagination {
            currentPage
            totalPages
            totalItems
        }
    }
}
"""

def fetch_products_from_qomra(search: str = ""):
    """
    جلب المنتجات مباشرة من قمرة وتنسيقها لتتوافق مع القالب اللحظي دون حفظ محلي.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QOMRA_API_TOKEN}" if QOMRA_API_TOKEN else ""
    }

    try:
        response = requests.post(
            QOMRA_GRAPHQL_URL,
            json={"query": PRODUCTS_QUERY},
            headers=headers,
            timeout=15
        )
        
        if response.status_code != 200:
            logger.error(f"❌ Qomra Fetch Failed [Status {response.status_code}]: {response.text}")
            raise Exception(f"فشل الاتصال بقمرة (رمز الاستجابة: {response.status_code})")

        payload = response.json()

        if "errors" in payload:
            logger.error(f"❌ GraphQL Validation Error: {payload['errors']}")
            raise Exception("حدث خطأ في استعلام قمرة")

        find_all_res = payload.get("data", {}).get("findAllProducts") or {}
        products_data = find_all_res.get("data") or []
        pagination_data = find_all_res.get("pagination") or {"currentPage": 1, "totalPages": 1, "totalItems": len(products_data)}

        # تصفية محلية سريعة بناءً على حقل البحث إذا وجد
        if search:
            products_data = [p for p in products_data if search.lower() in (p.get("title") or "").lower()]

        formatted_products = []
        for item in products_data:
            # معالجة الصور واستخراج fileUrl بأمان
            images_list = item.get("images") or []
            formatted_images = []
            for img in images_list:
                if isinstance(img, dict) and img.get("fileUrl"):
                    formatted_images.append({"fileUrl": img.get("fileUrl")})

            formatted_products.append({
                "qid": str(item.get("id")),
                "title": item.get("title") or "منتج بدون اسم",
                "description": item.get("description", ""),
                "sku": item.get("sku", ""),
                "quantity": int(item.get("quantity") or 0),
                "pricing": item.get("pricing") or {"price": 0.0},
                "images": formatted_images
            })

        pagination = {
            'currentPage': pagination_data.get("currentPage", 1),
            'totalPages': pagination_data.get("totalPages", 1),
            'totalItems': pagination_data.get("totalItems", len(formatted_products))
        }

        return formatted_products, pagination

    except Exception as e:
        logger.error(f"❌ Error fetching from Qomra: {str(e)}", exc_info=True)
        raise e

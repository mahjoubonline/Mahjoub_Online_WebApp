# coding: utf-8
# 📂 apps/utils/bridge_engine.py

import requests
import logging

logger = logging.getLogger(__name__)

# الرابط السيادي المباشر والصحيح والمطابق تماماً لإعدادات المنصة
QUMRA_API_URL = "https://mahjoub.online/admin/graphql"

def execute_query(query, variables=None):
    """
    المحرك الميكروي الأساسي والوحيد لإرسال استعلامات GraphQL حية ومباشرة.
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    try:
        response = requests.post(QUMRA_API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"GraphQL Endpoint Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Connection failed to GraphQL Endpoint: {str(e)}")
        return None

def get_products_by_supplier(tag="all"):
    """
    جلب المنتجات حياً بناءً على الوسم التابع للمورد (شريك النجاح).
    """
    # استعلام مبسط ونظيف لضمان التوافق الكامل وتجنب أخطاء الفلترة الصارمة
    query = """
    query {
        products {
            id
            title
            price
            image_url
        }
    }
    """
    result = execute_query(query)
    
    if result and "data" in result and "products" in result["data"]:
        all_products = result["data"]["products"]
        # فلترة المنتجات محلياً في بايثون لضمان عدم حدوث خطأ في سيرفر الـ GraphQL
        if tag and tag != "all":
            return [p for p in all_products if p.get("tag") == tag]
        return all_products
        
    return []

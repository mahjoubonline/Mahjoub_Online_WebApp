# coding: utf-8
# 📂 apps/utils/bridge_engine.py
import requests
import logging

logger = logging.getLogger(__name__)

# الرابط السيادي Sandbox المباشر والصحيح والمطابق تماماً لإعدادات الـ Sandbox
QUMRA_API_URL = "https://mahjoub.online/admin/graphql"

def execute_query(query, variables=None):
    """
    المحرك الميكروي الأساسي والوحيد لإرسال استعلامات GraphQL حية ومباشرة إلى متجر قمرة.
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
    جلب المنتجات حياً من قمرة بناءً على الوسم التابع للمورد (شريك النجاح).
    """
    # استعلام GraphQL مرن لجلب المنتجات
    query = """
    query getProducts($tag: String!) {
        products(filter: { tag: $tag }) {
            id
            title
            price
            image_url
        }
    }
    """
    variables = {"tag": tag}
    result = execute_query(query, variables)
    
    if result and "data" in result and "products" in result["data"]:
        return result["data"]["products"]
    
    return []

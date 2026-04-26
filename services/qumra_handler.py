import requests
import os

# جلب المفاتيح السيادية من متغيرات البيئة (Railway)
QUMRA_API_URL = os.getenv("QUMRA_API_URL")  # الرابط الذي ينتهي بـ /admin/graphql
QUMRA_TOKEN = os.getenv("QUMRA_API_KEY")    # التوكن qmr_...

def query_qumra(query, variables=None):
    """المحرك الأساسي لإرسال استعلامات GraphQL إلى قمرة"""
    headers = {
        "Authorization": f"Bearer {QUMRA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"query": query, "variables": variables}
    
    try:
        response = requests.post(QUMRA_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"🔴 فشل الاتصال بقمرة: {response.status_code}")
            return None
    except Exception as e:
        print(f"🔴 خطأ تقني في المحرك: {e}")
        return None

def fetch_qumra_collections():
    """جلب الأقسام من قمرة لتظهر للمورد كقائمة اختيار جاهزة"""
    query = """
    query {
      collections(first: 50) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    """
    result = query_qumra(query)
    if result and 'data' in result:
        # تحويل البيانات إلى تنسيق (ID, Name) لاستخدامها في Select Field
        return [
            (edge['node']['id'], edge['node']['name']) 
            for edge in result['data']['collections']['edges']
        ]
    return []

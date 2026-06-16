import requests
import json

# الرابط الأساسي للـ GraphQL
ENDPOINT = "https://mahjoub.online/admin/graphql"

# ضع الـ Token الخاص بك هنا (يفضل لاحقاً سحبه من متغيرات البيئة)
ACCESS_TOKEN = "ضع_الـ_TOKEN_الخاص_بك_هنا"

def execute_query(query, variables=None):
    """
    الدالة الأساسية لإرسال أي طلب (Query/Mutation) إلى قمرة
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
        
    try:
        response = requests.post(ENDPOINT, json=payload, headers=headers)
        response.raise_for_status() # للتأكد من عدم وجود أخطاء في الاتصال
        return response.json()
    except Exception as e:
        print(f"حدث خطأ في الاتصال بقمرة: {e}")
        return None

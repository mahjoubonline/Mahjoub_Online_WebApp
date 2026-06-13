# coding: utf-8
# 📂 apps/utils/bridge_engine.py - محرك المزامنة السيادي

import requests
from config import Config

class QumraBridgeEngine:
    """
    محرك المزامنة المسؤول عن الاتصال بـ GraphQL API الخاص بمتجر محجوب.
    يستخدم x-api-key للمصادقة ويوفر دوال لجلب المنتجات وبيانات المزامنة.
    """
    
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
        # تأكد أن المفتاح المستخدم في Config يملك صلاحية 'products:read'
        api_key = getattr(Config, 'QUMRA_API_KEY', '') or ""
        self.headers = {
            "x-api-key": str(api_key).strip(), 
            "Content-Type": "application/json",
            "apollo-require-preflight": "true" # تمت الإضافة لتجاوز حماية CSRF
        }

    def execute_query(self, query, variables=None):
        """
        تنفيذ أي استعلام GraphQL بشكل عام ومعالجة الأخطاء.
        """
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            # رفع استثناء إذا كان هناك خطأ في الاتصال (مثل 401, 403, 404, 500)
            response.raise_for_status()
            data = response.json()
            
            # فحص وجود أخطاء في استجابة GraphQL نفسها
            if "errors" in data:
                print(f"❌ GraphQL Errors: {data['errors']}")
                return {}
            
            return data if isinstance(data, dict) else {}
            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return {}
        except Exception as e:
            print(f"⚠️ Bridge Engine Error: {e}")
            return {}

    def fetch_latest_products(self, limit=10, page=1):
        """
        جلب قائمة المنتجات من النظام الخارجي.
        الاستعلام يعتمد على وجود صلاحية products:read في مفتاح الـ API.
        """
        query = """
        query GetProducts($limit: Int, $page: Int) {
            findAllProducts(input: { limit: $limit, page: $page }) {
                data {
                    title
                    quantity
                    pricing {
                        price
                    }
                }
            }
        }
        """
        variables = {"limit": limit, "page": page}
        result = self.execute_query(query, variables)
        
        # تحليل البيانات بأمان لتجنب ظهور أخطاء NoneType
        if not result or 'data' not in result:
            return []
            
        data_wrapper = result.get('data')
        if not isinstance(data_wrapper, dict):
            return []
            
        find_all = data_wrapper.get('findAllProducts')
        if not isinstance(find_all, dict):
            return []
            
        products = find_all.get('data')
        return products if isinstance(products, list) else []

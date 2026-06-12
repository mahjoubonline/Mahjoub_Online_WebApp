# coding: utf-8
import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
        # حماية ضد القيمة الفارغة (None)
        api_key = getattr(Config, 'QUMRA_API_KEY', '') or ""
        self.headers = {
            "x-api-key": str(api_key).strip(), 
            "Content-Type": "application/json"
        }

    def execute_query(self, query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️ Bridge Engine Error: {e}")
            return None # نرجع None بدلاً من القاموس ليتمكن الـ routes من التعامل معه

    def fetch_latest_products(self, limit=10, page=1):
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
        
        # حماية إضافية للبيانات القادمة
        if result and isinstance(result, dict) and 'data' in result:
            find_all = result['data'].get('findAllProducts')
            if find_all and isinstance(find_all, dict):
                return find_all.get('data', [])
        return []

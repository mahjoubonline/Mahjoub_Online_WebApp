# coding: utf-8
import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
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
            # التأكد من أن النتيجة قاموس دائماً
            data = response.json()
            return data if isinstance(data, dict) else {}
        except Exception as e:
            print(f"⚠️ Bridge Engine Error: {e}")
            return {}

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
        
        # استخدام .get() بأمان تام في كل خطوة
        # 1. نصل لـ 'data' من النتيجة الرئيسية
        data_wrapper = result.get('data')
        if not isinstance(data_wrapper, dict):
            return []
            
        # 2. نصل لـ 'findAllProducts' من داخل data
        find_all = data_wrapper.get('findAllProducts')
        if not isinstance(find_all, dict):
            return []
            
        # 3. نصل لـ 'data' (القائمة) من داخل findAllProducts
        products = find_all.get('data')
        
        # إرجاع القائمة إذا كانت موجودة وصحيحة، وإلا قائمة فارغة
        return products if isinstance(products, list) else []

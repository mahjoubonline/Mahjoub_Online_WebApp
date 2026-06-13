# coding: utf-8
# 📂 apps/utils/bridge_engine.py - محرك المزامنة السيادي (معدل للمصادقة)

import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        # الاحتمال الأكبر للخطأ 400 هو المسار. جرب إزالة /admin إذا كان الـ API عاماً
        self.endpoint = "https://mahjoub.online/graphql" 
        
        api_token = getattr(Config, 'QUMRA_API_KEY', '').strip()
        
        # تحسين الـ Headers لتكون أكثر توافقاً مع سيرفرات Apollo/GraphQL
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def execute_query(self, query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            
            # إذا استمر الخطأ 400، سيطبع لنا السيرفر السبب الحقيقي هنا
            if response.status_code != 200:
                print(f"DEBUG: Server rejected with Status {response.status_code}: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            if 'errors' in result:
                print(f"⚠️ GraphQL Errors: {result['errors']}")
            return result.get('data', {})
        except Exception as e:
            print(f"⚠️ Bridge Engine Connection Error: {e}")
            return {}

    def fetch_latest_products(self, limit=10, page=1):
        # استعلام مبسط جداً للاتصال
        query = """
        query GetProducts($limit: Int, $page: Int) {
            findAllProducts(input: { limit: $limit, page: $page }) {
                data {
                    title
                    quantity
                }
            }
        }
        """
        variables = {"limit": limit, "page": page}
        data = self.execute_query(query, variables)
        
        products = data.get('findAllProducts', {}).get('data', [])
        
        for p in products:
            p['auto_template'] = self.generate_product_html(p)
            
        return products if isinstance(products, list) else []

    def generate_product_html(self, product):
        return f"""
        <div class="product-snippet">
            <strong>{product.get('title', 'منتج')}</strong>
        </div>
        """

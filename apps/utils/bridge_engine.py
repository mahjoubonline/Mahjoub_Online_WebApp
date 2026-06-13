# coding: utf-8
# 📂 apps/utils/bridge_engine.py

import requests
import os

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
        api_token = os.environ.get('QUMRA_API_KEY', '').strip()
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def execute_query(self, query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=20)
            json_data = response.json()
            # 🔍 هذا السطر هو الأهم لكشف البنية
            print(f"DEBUG: RAW RESPONSE: {json_data}")
            return json_data
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            return {}

    def fetch_products(self, search_term="", page=1):
        query = """
        query($q: String, $page: Int) {
            findAllProducts(search: $q, page: $page) {
                data {
                    title
                    pricing { price }
                    quantity
                    status
                    images { fileUrl }
                }
            }
        }
        """
        variables = {"q": str(search_term), "page": int(page)}
        result = self.execute_query(query, variables=variables)
        
        # محاولة استخراج البيانات بمرونة
        root = result.get('data', {}).get('findAllProducts', {})
        products = root.get('data', []) if isinstance(root, dict) else []
        
        processed_products = []
        for p in products:
            pricing = p.get('pricing') or {}
            images = p.get('images') or []
            img_url = images[0].get('fileUrl') if images and isinstance(images, list) else None
            
            processed_products.append({
                'title': p.get('title'),
                'price': pricing.get('price', 0),
                'quantity': p.get('quantity', 0),
                'status': p.get('status'),
                'image_url': img_url
            })
        return processed_products

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
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ DEBUG: Status {response.status_code} | Body: {response.text}")
                return {}
            
            result = response.json()
            
            if 'errors' in result:
                print(f"❌ GraphQL Errors: {result['errors']}")
                return {}
                
            return result.get('data', {})
            
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            return {}

    def fetch_latest_products(self):
        # الاستعلام المصحح مع طلب الحقول الفرعية المطلوبة
        query = """
        query {
            findAllProducts {
                data {
                    title
                    pricing {
                        price
                    }
                    quantity
                    status
                    images {
                        src
                    }
                }
            }
        }
        """
        data = self.execute_query(query)
        
        # استخراج البيانات من المسار المكتشف
        products = data.get('findAllProducts', {}).get('data', [])
        
        # تحويل البيانات لتناسب توقعات القالب (Template)
        for p in products:
            # استخراج السعر من كائن pricing
            pricing = p.get('pricing')
            p['price'] = pricing.get('price') if isinstance(pricing, dict) else 0
            
            # استخراج رابط الصورة الأول من قائمة images
            images = p.get('images')
            if isinstance(images, list) and len(images) > 0:
                p['image_url'] = images[0].get('src')
            else:
                p['image_url'] = None
                
        return products

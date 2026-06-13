# coding: utf-8
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

    def execute_query(self, query):
        try:
            response = requests.post(self.endpoint, json={"query": query}, headers=self.headers, timeout=15)
            return response.json()
        except Exception as e:
            return {"errors": [{"message": str(e)}]}

    def fetch_latest_products(self):
        # استعلام كشف حقول ImageProduct
        introspection_query = """
        query {
            __type(name: "ImageProduct") {
                fields { name }
            }
        }
        """
        debug_data = self.execute_query(introspection_query)
        print(f"DEBUG: ImageProduct Fields Discovery: {debug_data}")

        # استعلام لجلب المنتجات بدون الحقل المسبب للخطأ لنتمكن من رؤية البيانات المتاحة
        query = """
        query {
            findAllProducts {
                data {
                    title
                    pricing { price }
                    quantity
                    status
                    images { 
                        # سنعرف الاسم الصحيح من الـ Logs بناءً على نتيجة الاستعلام أعلاه
                        url 
                    } 
                }
            }
        }
        """
        data = self.execute_query(query)
        print(f"DEBUG: Products Query Result: {data}")
        return []

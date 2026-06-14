# 📂 apps/utils/bridge_engine.py
import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = Config.QUMRA_API_URL
        self.headers = {
            "Authorization": f"Bearer {Config.QUMRA_API_KEY}",
            "Content-Type": "application/json",
            "apollo-require-preflight": "true"
        }

    def fetch_products_from_qumra(self, search_term="", page=1):
        """
        جلب البيانات من قمرة مع دعم البحث والترقيم (Pagination).
        """
        # نحدد عدد العناصر في كل صفحة (مثلاً 20 منتج)
        limit = 20
        offset = (page - 1) * limit

        # استعلام GraphQL مع دعم الترقيم والفلترة
        query = """
        query($q: String, $limit: Int, $offset: Int) {
            findAllProducts(filter: { title: $q }, limit: $limit, offset: $offset) {
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
        
        try:
            response = requests.post(
                self.endpoint, 
                json={
                    "query": query, 
                    "variables": {"q": search_term, "limit": limit, "offset": offset}
                }, 
                headers=self.headers, 
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json().get('data', {}).get('findAllProducts', {}).get('data', [])
                
                formatted_products = []
                for p in result:
                    img = p.get('images', [])
                    formatted_products.append({
                        'title': p.get('title', 'بدون عنوان'),
                        'price': p.get('pricing', {}).get('price', 0),
                        'quantity': p.get('quantity', 0),
                        'status': p.get('status', 'N/A'),
                        'image_url': img[0].get('fileUrl') if img and isinstance(img, list) else None
                    })
                return formatted_products
            
            else:
                print(f"❌ API Error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Bridge Exception: {str(e)}")
            return []

    def sync_all_data(self):
        return True

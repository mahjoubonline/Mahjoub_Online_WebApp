# 📂 apps/utils/bridge_engine.py
import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = Config.QUMRA_API_URL
        self.headers = {
            "Authorization": f"Bearer {Config.QUMRA_API_KEY}",
            "Content-Type": "application/json"
        }

    def fetch_products_from_qumra(self, search_term="", page=1):
        # سنحاول جلب البيانات بدون فلتر معقد في البداية للتأكد من نجاح الاتصال
        # إذا نجح هذا، سنعرف أن المشكلة كانت في صيغة الفلتر
        query = """
        query {
            findAllProducts {
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
                json={"query": query}, 
                headers=self.headers, 
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json().get('data', {}).get('findAllProducts', {}).get('data', [])
                
                # الفلترة الآن تتم برمجياً هنا للتأكد من عمل البحث حتى لو رفض السيرفر الفلتر
                if search_term:
                    data = [p for p in data if search_term.lower() in p.get('title', '').lower()]
                
                return data
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return []

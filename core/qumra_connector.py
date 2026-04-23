import requests
import os
from .models import db, Product, Supplier

class QumraSync:
    def __init__(self):
        self.api_key = os.environ.get('QUMRA_API_KEY')
        self.api_url = os.environ.get('QUMRA_API_URL')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def fetch_and_sync(self):
        """جلب المنتجات من قمرة وتخزينها في Render"""
        if not self.api_key or not self.api_url:
            return False, "بيانات الربط مع قمرة مفقودة في إعدادات رويال"

        try:
            # طلب البيانات من قمرة (هنا نستخدم GraphQL كما يظهر في رابطك)
            query = """
            {
              products(first: 10) {
                nodes {
                  id
                  name
                  price
                }
              }
            }
            """
            response = requests.post(self.api_url, json={'query': query}, headers=self.headers)
            data = response.json()

            products = data.get('data', {}).get('products', {}).get('nodes', [])
            
            for item in products:
                # التأكد إذا كان المنتج موجوداً مسبقاً لتحديثه أو إضافته
                existing = Product.query.filter_by(qumra_id=item['id']).first()
                if not existing:
                    new_prod = Product(
                        qumra_id=item['id'],
                        name=item['name'],
                        price=float(item['price'])
                    )
                    db.session.add(new_prod)
            
            db.session.commit()
            return True, f"تمت مزامنة {len(products)} منتج بنجاح!"
        
        except Exception as e:
            return False, f"خطأ أثناء المزامنة: {str(e)}"

qumra_manager = QumraSync()

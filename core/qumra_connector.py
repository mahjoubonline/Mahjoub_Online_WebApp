import requests
import os
from .models import db, Product, Supplier

class QumraSync:
    def __init__(self):
        # سحب البيانات من متغيرات Railway
        self.api_key = os.environ.get('QUMRA_API_KEY')
        self.api_url = os.environ.get('QUMRA_API_URL')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def fetch_and_sync(self):
        """جلب المنتجات من قمرة وتخزينها في Render"""
        if not self.api_key or not self.api_url:
            return False, "بيانات الربط مفقودة (API Key أو URL)"

        try:
            # استعلام GraphQL (تأكد من مطابقة الحقول لما في Apollo Sandbox)
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
            response = requests.post(self.api_url, json={'query': query}, headers=self.headers, timeout=15)
            
            # التحقق من نجاح الطلب
            if response.status_code != 200:
                return False, f"فشل الاتصال بقمرة (كود: {response.status_code})"

            data = response.json()
            products = data.get('data', {}).get('products', {}).get('nodes', [])
            
            if not products:
                return True, "لا توجد منتجات جديدة لجلبها حالياً."
            
            count = 0
            for item in products:
                # تحديث إذا كان موجوداً، أو إضافة إذا كان جديداً
                existing = Product.query.filter_by(qumra_id=item['id']).first()
                if existing:
                    existing.name = item.get('name', existing.name)
                    existing.price = float(item.get('price', existing.price))
                else:
                    new_prod = Product(
                        qumra_id=item['id'],
                        name=item['name'],
                        price=float(item['price'])
                    )
                    db.session.add(new_prod)
                count += 1
            
            db.session.commit()
            return True, f"✅ تمت مزامنة {count} منتج بنجاح!"
        
        except Exception as e:
            db.session.rollback()
            return False, f"❌ خطأ أثناء المزامنة: {str(e)}"

# هذا الكائن هو ما يستدعيه ملف admin_panel/routes.py
qumra_manager = QumraSync()

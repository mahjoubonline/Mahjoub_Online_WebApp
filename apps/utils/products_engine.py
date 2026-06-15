# 📂 apps/utils/products_engine.py
from apps.utils.bridge_engine import QumraBridgeEngine

class ProductsEngine(QumraBridgeEngine):
    def fetch_all(self, search_term="", page=1):
        # الاستعلام هنا مخصص للمنتجات فقط
        query = """
        query {
            findAllProducts {
                title
                pricing { price }
                quantity
                status
                images { fileUrl }
            }
        }
        """
        result = self.execute_query(query)
        
        if not result or 'data' not in result:
            return []

        raw_products = result.get('data', {}).get('findAllProducts', [])
        
        # معالجة البيانات
        all_products = []
        for p in raw_products:
            images = p.get('images', [])
            all_products.append({
                "title": p.get('title', 'بدون اسم'),
                "price": p.get('pricing', {}).get('price', 0),
                "quantity": p.get('quantity', 0),
                "image_url": images[0].get('fileUrl') if images else 'https://via.placeholder.com/150',
                "status": p.get('status', 'غير محدد')
            })

        # فلترة وترقيم برمجياً
        if search_term:
            all_products = [p for p in all_products if search_term.lower() in p['title'].lower()]
        
        per_page = 20
        start = (page - 1) * per_page
        return all_products[start:start + per_page]

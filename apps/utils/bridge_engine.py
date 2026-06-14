# coding: utf-8
import requests
import os
import time

# ذاكرة مؤقتة للمنتجات
_CACHE = {"products": [], "last_updated": 0}
CACHE_TIMEOUT = 3600  # تحديث تلقائي كل ساعة

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('QUMRA_API_KEY', '').strip()}",
            "Content-Type": "application/json"
        }

    def fetch_products(self, search_term="", page=1):
        # 1. تحديث البيانات إذا انتهت صلاحية الكاش أو كان فارغاً
        if not _CACHE["products"] or (time.time() - _CACHE["last_updated"] > CACHE_TIMEOUT):
            self.sync_all_data()
        
        # 2. البحث والفلترة محلياً (فائق السرعة)
        all_data = _CACHE["products"]
        if search_term:
            s = search_term.lower()
            all_data = [p for p in all_data if s in (p.get('title') or "").lower()]
            
        # 3. الترقيم (Pagination)
        start = (page - 1) * 16
        return all_data[start : start + 16]

    def sync_all_data(self):
        """جلب كامل البيانات من قمرة وتحديث الكاش"""
        query = "query { findAllProducts { data { title pricing { price } quantity status images { fileUrl } } } }"
        try:
            response = requests.post(self.endpoint, json={"query": query}, headers=self.headers, timeout=20)
            data = response.json().get('data', {}).get('findAllProducts', {}).get('data', [])
            
            # معالجة البيانات وتخزينها
            processed = []
            for p in data:
                img = p.get('images', [])
                processed.append({
                    'title': p.get('title'),
                    'price': p.get('pricing', {}).get('price', 0),
                    'quantity': p.get('quantity', 0),
                    'status': p.get('status'),
                    'image_url': img[0].get('fileUrl') if img else None
                })
            
            _CACHE["products"] = processed
            _CACHE["last_updated"] = time.time()
            return True
        except Exception as e:
            print(f"Sync Error: {e}")
            return False

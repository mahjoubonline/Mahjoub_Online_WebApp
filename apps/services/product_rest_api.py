# coding: utf-8
# 📂 apps/services/product_rest_api.py

import requests
import os
import json

class ProductRestAPI:
    def __init__(self):
        self.api_key = os.environ.get('QUMRA_API_KEY')
        self.base_url = "https://mahjoub.online"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    # ============================================================
    # ✅ رفع صورة إلى مكتبة قمرة
    # ============================================================
    def upload_image(self, image_data: bytes, filename: str) -> str:
        """
        رفع صورة إلى مكتبة قمرة
        
        Args:
            image_data: بيانات الصورة (bytes)
            filename: اسم الملف
        
        Returns:
            str: رابط الصورة في قمرة
        """
        # ✅ جرب عدة Endpoints للرفع
        endpoints = [
            f"{self.base_url}/api/upload",
            f"{self.base_url}/admin/api/upload",
            f"{self.base_url}/api/media",
            f"{self.base_url}/admin/api/media",
            f"{self.base_url}/api/images",
        ]
        
        files = {
            'file': (filename, image_data, 'image/jpeg')
        }
        
        for url in endpoints:
            try:
                print(f"🔍 محاولة رفع الصورة إلى: {url}")
                response = requests.post(
                    url,
                    files=files,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30
                )
                print(f"   Status: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    image_url = data.get('url') or data.get('data', {}).get('fileUrl') or data.get('fileUrl')
                    if image_url:
                        print(f"✅ تم رفع الصورة: {image_url}")
                        return image_url
            except Exception as e:
                print(f"   ❌ خطأ: {e}")
                continue
        
        print("❌ فشل رفع الصورة في جميع الـ Endpoints")
        return None
    
    # ============================================================
    # ✅ إنشاء منتج
    # ============================================================
    def create_product(self, product_data: dict) -> dict:
        """إنشاء منتج جديد في قمرة"""
        endpoints = [
            f"{self.base_url}/api/products",
            f"{self.base_url}/admin/api/products",
            f"{self.base_url}/products",
            f"{self.base_url}/admin/products",
        ]
        
        for url in endpoints:
            try:
                print(f"🔍 محاولة إنشاء منتج إلى: {url}")
                response = requests.post(
                    url,
                    json=product_data,
                    headers=self.headers,
                    timeout=30
                )
                print(f"   Status: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    qid = data.get('qid') or data.get('data', {}).get('qid')
                    return {
                        'success': True,
                        'qid': qid,
                        'message': 'تم إنشاء المنتج بنجاح'
                    }
            except Exception as e:
                print(f"   ❌ خطأ: {e}")
                continue
        
        return {
            'success': False,
            'message': 'جميع الـ Endpoints فشلت',
            'qid': None
        }
    
    # ============================================================
    # ✅ تحديث منتج
    # ============================================================
    def update_product(self, qid: str, product_data: dict) -> bool:
        """تحديث منتج في قمرة"""
        endpoints = [
            f"{self.base_url}/api/products/{qid}",
            f"{self.base_url}/admin/api/products/{qid}",
            f"{self.base_url}/products/{qid}",
        ]
        
        for url in endpoints:
            try:
                response = requests.put(url, json=product_data, headers=self.headers, timeout=30)
                if response.status_code in [200, 201]:
                    return True
            except:
                continue
        return False
    
    # ============================================================
    # ✅ حذف منتج
    # ============================================================
    def delete_product(self, qid: str) -> bool:
        """حذف منتج من قمرة"""
        endpoints = [
            f"{self.base_url}/api/products/{qid}",
            f"{self.base_url}/admin/api/products/{qid}",
            f"{self.base_url}/products/{qid}",
        ]
        
        for url in endpoints:
            try:
                response = requests.delete(url, headers=self.headers, timeout=30)
                if response.status_code in [200, 204]:
                    return True
            except:
                continue
        return False

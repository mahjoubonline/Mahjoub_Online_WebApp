from apps import db
from datetime import datetime
from cryptography.fernet import Fernet
import os

def get_or_create_key():
    """الحصول على المفتاح من البيئة وتأمين تحويله إلى بايتات"""
    key = os.environ.get('ENCRYPTION_KEY')
    
    if key:
        # إذا كان المفتاح موجوداً كـ string من Environment Variables
        # نحوله إلى بايتات بطريقة آمنة
        return key.encode('utf-8')
    
    # في حال عدم وجوده، نولد مفتاحاً جديداً (للتطوير المحلي)
    new_key = Fernet.generate_key()
    print(f"⚠️ WARNING: No ENCRYPTION_KEY found. Generated: {new_key.decode('utf-8')}")
    return new_key

# تهيئة التشفير بمفتاح آمن
KEY = get_or_create_key()
cipher_suite = Fernet(KEY)

def encrypt(value):
    if value is None: return None
    # تأكد من تحويل القيمة لنص ثم بايتات
    return cipher_suite.encrypt(str(value).encode('utf-8')).decode('utf-8')

def decrypt(value):
    if value is None: return None
    try:
        # فك التشفير وإعادة تحويل البايتات لنص
        return cipher_suite.decrypt(value.encode('utf-8')).decode('utf-8')
    except Exception:
        # في حال حدوث خطأ (مثل مفتاح مختلف)، نعيد قيمة صفرية
        return "0.0"

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # حقول مشفرة (Data at Rest)
    _encrypted_price = db.Column(db.String(500), nullable=True)
    _encrypted_cost = db.Column(db.String(500), nullable=True)
    
    status = db.Column(db.String(50), default='draft')
    quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500), nullable=True)
    supplier_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def price(self):
        return float(decrypt(self._encrypted_price)) if self._encrypted_price else 0.0

    @price.setter
    def price(self, value):
        self._encrypted_price = encrypt(value)

class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    option1_name = db.Column(db.String(50), nullable=True)
    option1_value = db.Column(db.String(50), nullable=True)
    
    _encrypted_variant_price = db.Column(db.String(500), nullable=True)
    variant_quantity = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(100), nullable=True)

    @property
    def variant_price(self):
        return float(decrypt(self._encrypted_variant_price)) if self._encrypted_variant_price else 0.0

    @variant_price.setter
    def variant_price(self, value):
        self._encrypted_variant_price = encrypt(value)

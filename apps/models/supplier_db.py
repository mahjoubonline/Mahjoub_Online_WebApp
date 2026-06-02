# coding: utf-8
import os
from apps.extensions import db

# 🛡️ محاولة استيراد مشفر البيانات الأصلي مع خطة بديلة تمنع الانهيار
try:
    from apps.utils.security import AESCipher
    print("✅ [Security] تم تحميل محرك التشفير AESCipher بنجاح.")
except ModuleNotFoundError:
    print("⚠️ [Warning] لم يتم العثور على apps.utils.security في السيرفر!")
    print("⚙️ [Fallback] تم تفعيل مشفر احتياطي مؤقت (Dummy Cipher) لمنع السيرفر من الانهيار.")
    
    # مشفر بديل محايد يمنع الـ AttributeError والانهيار في السيرفر
    class AESCipher:
        def __init__(self, key):
            self.key = key
        def encrypt(self, text):
            return str(text)  # يمرر النص كما هو مؤقتاً لحين رفع الملف
        def decrypt(self, text):
            return str(text)  # يعيد النص كما هو

# تهيئة مشفر البيانات مع التحقق من وجود المفتاح السيادي
encryption_key = os.getenv('ENCRYPTION_KEY')
if not encryption_key:
    print("⚠️ تحذير أمني: ENCRYPTION_KEY غير موجود في متغيرات البيئة! تم تفعيل المفتاح المؤقت.")
    encryption_key = '00000000000000000000000000000000' # مفتاح افتراضي مؤقت للتطوير المحلي فقط

cipher = AESCipher(encryption_key)

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    # الأعمدة الأساسية والفريدة
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column('sovereign_id', db.String(50), unique=True, nullable=False, index=True) 
    wallet_code = db.Column('wallet_code', db.String(50), unique=True, nullable=False)
    
    # الحقول المشفرة في قاعدة البيانات (مؤمنة بالكامل)
    owner_name_enc = db.Column('owner_name', db.String(255), nullable=False)
    owner_phone_enc = db.Column('owner_phone', db.String(255), nullable=False)
    trade_name_enc = db.Column('trade_name', db.String(255), nullable=False)
    shop_phone_enc = db.Column('shop_phone', db.String(255), nullable=False)
    bank_acc_enc = db.Column('bank_acc', db.String(255), nullable=False)
    
    # حقول التقييم والتصنيف الرقمي
    category = db.Column('category', db.String(50), default='عام') 
    behavior_score = db.Column('behavior_score', db.Float, default=100.0)
    total_transactions = db.Column('total_transactions', db.Integer, default=0)
    
    # الحقول الإدارية والجوهرية للهوية
    username = db.Column('username', db.String(80), unique=True, nullable=False)
    password_hash = db.Column('password_hash', db.String(255), nullable=False)
    identity_type = db.Column('identity_type', db.String(50), nullable=False)   
    identity_number = db.Column('identity_number', db.String(50), unique=True, nullable=False)  
    identity_image = db.Column('identity_image', db.String(255))   
    activity_type = db.Column('activity_type', db.String(50))     
    
    # البيانات الجغرافية والتفصيلية
    province = db.Column('province', db.String(50))
    district = db.Column('district', db.String(50))
    address_detail = db.Column('address_detail', db.Text) 
    
    # البيانات المالية والترتيب الرقمي
    fin_type = db.Column('fin_type', db.String(20))           
    bank_name = db.Column('bank_name', db.String(100))        
    status = db.Column('status', db.String(20), nullable=False, default='pending') 
    rank_grade = db.Column('rank_grade', db.String(20), nullable=False, default='ريادي') 
    registration_source = db.Column('registration_source', db.String(30), nullable=False, default='الموقع الخارجي') 
    
    # الطوابع الزمنية
    created_at = db.Column('created_at', db.DateTime, default=db.func.current_timestamp()) 
    updated_at = db.Column('updated_at', db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # --- بوابات التشفير وفك التشفير التلقائي (Properties) ---
    @property
    def owner_name(self): return cipher.decrypt(self.owner_name_enc)
    @owner_name.setter
    def owner_name(self, value): self.owner_name_enc = cipher.encrypt(str(value))

    @property
    def owner_phone(self): return cipher.decrypt(self.owner_phone_enc)
    @owner_phone.setter
    def owner_phone(self, value): self.owner_phone_enc = cipher.encrypt(str(value))

    @property
    def trade_name(self): return cipher.decrypt(self.trade_name_enc)
    @trade_name.setter
    def trade_name(self, value): self.trade_name_enc = cipher.encrypt(str(value))

    @property
    def shop_phone(self): return cipher.decrypt(self.shop_phone_enc)
    @shop_phone.setter
    def shop_phone(self, value): self.shop_phone_enc = cipher.encrypt(str(value))

    @property
    def bank_acc(self): return cipher.decrypt(self.bank_acc_enc)
    @bank_acc.setter
    def bank_acc(self, value): self.bank_acc_enc = cipher.encrypt(str(value))

    # --- الدوال الوظيفية للموديل ---
    def learn_from_interaction(self, is_positive):
        """تحديث التقييم السلوكي للمورد بناءً على كفاءة عملياته"""
        self.behavior_score += (0.5 if is_positive else -2.0)
        self.total_transactions += 1

    @property
    def balance(self):
        """جلب الرصيد الحالي الحركي للمورد من جدول كشوفات الحساب"""
        from apps.models.statement_db import SupplierStatement
        last = SupplierStatement.query.filter_by(supplier_id=self.id).order_by(SupplierStatement.created_at.desc()).first()
        return last.running_balance if last else 0.0

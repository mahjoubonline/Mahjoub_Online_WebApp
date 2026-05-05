# core/models/supplier.py
import os
import sys
from datetime import datetime

# --- بروتوكول تثبيت المسار الجذري ---
# نقوم بإضافة مجلد 'app' (الذي يحتوي على core) إلى مسار النظام
# لضمان أن 'from core.extensions' تعمل في Railway
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- استيراد قاعدة البيانات (db) ---
# نستخدم try-except لتغطية كافة احتمالات تشغيل السيرفر
try:
    from core.extensions import db
except ImportError:
    try:
        from ..extensions import db
    except ImportError:
        # الملاذ الأخير إذا فشلت المسارات المنظمة
        from extensions import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    owner_name = db.Column(db.String(150), nullable=False)
    trade_name = db.Column(db.String(150), nullable=False)
    activity_type = db.Column(db.String(100))
    id_type = db.Column(db.String(50))
    id_card_number = db.Column(db.String(50))
    phone = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address_detail = db.Column(db.Text)
    e_wallet = db.Column(db.String(100), unique=True)
    bank_name = db.Column(db.String(100))
    bank_acc = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Supplier {self.trade_name}>'

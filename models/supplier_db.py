from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True, nullable=False) # المعرف الموحد
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # بيانات المنشأة
    trade_name = db.Column(db.String(150), unique=True, nullable=False)
    owner_name = db.Column(db.String(150), nullable=False)
    identity_type = db.Column(db.String(50))
    identity_number = db.Column(db.String(50))
    identity_image = db.Column(db.String(255)) # مسار الصورة
    
    # التواصل والموقع
    shop_phone = db.Column(db.String(20), unique=True, nullable=False)
    province = db.Column(db.String(50))
    district = db.Column(db.String(50))
    address_detail = db.Column(db.Text)
    
    # البيانات المالية
    fin_type = db.Column(db.String(20)) # بنوك أو صرافة
    bank_name = db.Column(db.String(100))
    bank_acc = db.Column(db.String(50))
    activity_type = db.Column(db.String(50)) # جملة أو تجزئة
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

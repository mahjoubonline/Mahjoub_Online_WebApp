from core import db
from datetime import datetime

class AdminLog(db.Model):
    """
    سجل العمليات السيادية - لمراقبة تحركات الإدارة داخل المنصة.
    """
    __tablename__ = 'admin_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False) # وصف العملية (مثلاً: تعميد مورد)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))

    def __repr__(self):
        return f'<AdminLog {self.action} by Admin {self.admin_id}>'

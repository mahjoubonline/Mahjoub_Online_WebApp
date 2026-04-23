# admin_panel/models.py

# نحن لا نعرف الجداول هنا من الصفر، بل نستوردها من المركز 
# لضمان أن النظام يقرأ من نفس قاعدة بيانات Render
from core.models import db, Supplier, Product

# يمكنك إضافة جداول خاصة فقط بالإدارة هنا مستقبلاً
# مثل جداول سجلات عمليات المدير (AdminLogs)
class AdminLog(db.Model):
    __tablename__ = 'admin_logs'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    admin_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class AdminSettlement(db.Model):
    """
    جدول مخصص حصرياً لإدارة وتوثيق التسويات المالية الإدارية والاستثنائية
    يرتبط بكل نافذة تسوية وحوكمة في لوحة التحكم المركزية
    """
    __tablename__ = 'admin_settlements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    
    # تفاصيل الحوكمة والنوعية
    settlement_code = db.Column(db.String(60), unique=True, nullable=False) # رمز السند المالي للتسوية
    settlement_type = db.Column(db.String(30), nullable=False) # إيداع شحن / خصم عكسي / تسوية معلق
    currency = db.Column(db.String(10), nullable=False)        # YER / SAR / USD
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    
    # التوثيق البنكي والمرجعي
    financial_entity = db.Column(db.String(100), default="إدارة المنصة المركزية", nullable=True) # البنك أو شركة الصرافة
    reference_number = db.Column(db.String(100), default="SETTLE-ADMIN", nullable=True)         # رقم الحوالة أو السند
    
    # البيانات الحسابية التفسيرية
    reason_notes = db.Column(db.Text, nullable=False) # سبب التسوية (شرط أساسي للحوكمة لمنع التلاعب)
    created_by = db.Column(db.String(50), nullable=True) # معرف الإداري الذي قام بالتسوية
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @staticmethod
    def generate_settlement_code():
        """ توليد رمز مالي فريد ومحمي خاص بسندات التسوية الإدارية """
        import random
        return f"STL-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

    def __repr__(self):
        return f"<AdminSettlement {self.settlement_code} | Type {self.settlement_type} | {self.amount} {self.currency}>"

# ... (نفس الاستيرادات السابقة)
from sqlalchemy import event

class Supplier(db.Model):
    # ... (نفس الحقول التي أرسلتها بدون تغيير)

    # --- بروتوكولات الحماية والتعميد المحدثة ---

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def mint_sovereign_id(self):
        """توليد المعرف السيادي بنمط 9631، 9632..."""
        if self.id:
            tag = f"963{self.id}" 
            self.e_wallet = f"WAL_MAH_{tag}"
            self.sovereign_id = f"SUP_MAH_{tag}"
            return self.sovereign_id
        return None

    # --- إضافة ذكاء الأرصدة (Total Value) ---
    def get_total_balance_in_yer(self, sar_rate, usd_rate):
        """حساب إجمالي الثروة بالريال اليمني بناءً على صرف المحرك"""
        return float(self.balance_yer) + (float(self.balance_sar) * sar_rate) + (float(self.balance_usd) * usd_rate)

    # ... (بقية الدوال: get_status_color و to_dict كما هي)

# --- محرك التعميد التلقائي (Sovereign Auto-Mint) ---
@event.listens_for(Supplier, 'after_insert')
def receive_after_insert(mapper, connection, target):
    """بمجرد دخول المورد للقاعدة، يتم منحه الهوية السيادية فوراً"""
    table = Supplier.__table__
    tag = f"963{target.id}"
    connection.execute(
        table.update().
        where(table.c.id == target.id).
        values(
            sovereign_id=f"SUP_MAH_{tag}",
            e_wallet=f"WAL_MAH_{tag}"
        )
    )

from apps import create_app
from apps.extensions import db
from sqlalchemy import text, inspect

app = create_app()

def fix_database():
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            # 1. إصلاح جدول المحافظ
            cols_wallets = [c['name'] for c in inspector.get_columns('supplier_wallets')]
            for col in ['_yer_total', '_sar_total', '_usd_total']:
                if col not in cols_wallets:
                    db.session.execute(text(f"ALTER TABLE supplier_wallets ADD COLUMN {col} VARCHAR(255)"))
            
            # 2. إصلاح جدول المعاملات
            cols_tx = [c['name'] for c in inspector.get_columns('wallet_transactions')]
            for col in ['_amount', '_profit_margin', '_notes']:
                if col not in cols_tx:
                    db.session.execute(text(f"ALTER TABLE wallet_transactions ADD COLUMN {col} VARCHAR(255)"))
            
            db.session.commit()
            print("✅ Database structure fixed successfully.")
        except Exception as e:
            print(f"⚠️ Fix failed: {e}")
            db.session.rollback()

# استدعاء الإصلاح
fix_database()

if __name__ == "__main__":
    app.run()

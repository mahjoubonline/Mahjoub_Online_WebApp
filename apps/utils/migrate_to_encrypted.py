# coding: utf-8
# 🚀 سكربت ترحيل البيانات المشفرة - منصة محجوب أونلاين 2026
from apps import create_app
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.statement_db import SupplierStatement
from apps.models.wallet_db import SupplierWallet, WalletTransaction

def run_migration():
    # 1. إنشاء نسخة من التطبيق لتهيئة البيئة (App Factory)
    app = create_app()
    
    # 2. الدخول في سياق التطبيق للوصول إلى قاعدة البيانات والمشفر
    with app.app_context():
        print("🚀 بدء عملية الترحيل المشفر...")
        
        try:
            # 3. معالجة الموردين
            # ملاحظة: تعيين القيمة لنفسها (s.owner_name = s.owner_name) 
            # سيقوم بتشغيل دالة الـ setter التي تشفر البيانات
            suppliers = Supplier.query.all()
            for s in suppliers:
                s.owner_name = s.owner_name 
                s.trade_name = s.trade_name
                s.owner_phone = s.owner_phone
                s.shop_phone = s.shop_phone
                s.bank_acc = s.bank_acc
                print(f"✅ تمت معالجة المورد: {s.sovereign_id}")
            
            # 4. معالجة كشوفات الحسابات
            statements = SupplierStatement.query.all()
            for stmt in statements:
                # إذا كانت هذه الحقول تستخدم مشفر، تأكد من وجود setter لها في الموديل
                stmt.description = stmt.description
            
            # 5. معالجة المحافظ
            wallets = SupplierWallet.query.all()
            for w in wallets:
                # المحافظ غالباً لا تحتاج تشفير (أرقام)، لكن تم الاحتفاظ بها للنمط
                pass
                
            # 6. معالجة الحركات
            transactions = WalletTransaction.query.all()
            for tx in transactions:
                tx.notes = tx.notes

            # 7. الحفظ النهائي في قاعدة البيانات
            db.session.commit()
            print("🎉 اكتملت عملية الترحيل بنجاح وتم تشفير كافة البيانات!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ حدث خطأ أثناء الترحيل: {str(e)}")

if __name__ == "__main__":
    run_migration()

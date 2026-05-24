# coding: utf-8
# 💳 مستند العمليات والتحكم المالي الموحد - منصة محجوب أونلاين 2026

from flask import render_template, request
from sqlalchemy import func, text
from apps import db
from apps.wallet import wallet_blueprint
from apps.models.wallet_db import SupplierWallet, WalletTransaction

def ensure_columns_exist_safely():
    """
    محرك فحص وحقن الأعمدة الثلاثية بشكل مستقل لكل عمود على حدة.
    تقوم بعمل rollback فوري عند تكرار العمود لتفادي تجميد وإجهاض الجلسة (Transaction Abort).
    """
    required_columns = [
        ("yer_total", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("yer_withdrawn", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("yer_pending", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("sar_total", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("sar_withdrawn", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("sar_pending", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("usd_total", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("usd_withdrawn", "NUMERIC(15, 2) DEFAULT 0.00"),
        ("usd_pending", "NUMERIC(15, 2) DEFAULT 0.00")
    ]
    
    for col_name, col_type in required_columns:
        try:
            # فتح اتصال مستقل لكل عمود لحماية الجلسة العامة
            with db.engine.begin() as connection:
                connection.execute(text(f"ALTER TABLE supplier_wallets ADD COLUMN {col_name} {col_type};"))
                print(f"✅ تم حقن العمود بنجاح: {col_name}")
        except Exception:
            # إذا كان العمود موجوداً مسبقاً، Postgres ستفشل، نقوم بالتخطي الآمن والصامت دون إجهاض المنظومة
            continue

@wallet_blueprint.route('/admin/overview', methods=['GET'])
def overview():
    # 1. تفعيل محرك الفحص الذكي وحقن الأعمدة لضمان استقرار الاستعلامات
    ensure_columns_exist_safely()

    search_query = request.args.get('search_query', '').strip()
    
    # 2. حساب الإحصائيات المالية الإجمالية لكافة المحافظ الشاملة بالنظام
    try:
        total_wallets_count = SupplierWallet.query.count()
        total_yer = db.session.query(func.sum(SupplierWallet.yer_total)).scalar() or 0.00
        total_sar = db.session.query(func.sum(SupplierWallet.sar_total)).scalar() or 0.00
        total_usd = db.session.query(func.sum(SupplierWallet.usd_total)).scalar() or 0.00
    except Exception:
        # حماية وقائية في حال لم تكتمل الهجرة اللحظية بعد
        total_wallets_count = 0
        total_yer = total_sar = total_usd = 0.00

    wallet = None
    transactions = []

    # 3. محرك الفلترة والبحث المتقدم واستدعاء شركاء النجاح
    if search_query:
        wallet = SupplierWallet.query.filter(
            (SupplierWallet.supplier_id == search_query) | 
            (SupplierWallet.wallet_code == search_query)
        ).first()
        
        if wallet:
            transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id).order_by(WalletTransaction.created_at.desc()).all()
    else:
        # عند الضغط على "عرض الجميع" أو الإقلاع الأول، يظهر النظام أول محفظة مع أحدث الحركات العامة
        wallet = SupplierWallet.query.first()
        transactions = WalletTransaction.query.order_by(WalletTransaction.created_at.desc()).limit(50).all()

    # 4. تمرير الأرشفة والبيانات الكاملة للواجهة الرسومية الباهرة
    return render_template(
        'admin/overview.html',
        wallet=wallet,
        transactions=transactions,
        current_search=search_query,
        total_wallets_count=total_wallets_count,
        total_yer_system=total_yer,
        total_sar_system=total_sar,
        total_usd_system=total_usd
    )

# coding: utf-8
# 📊 لوحة التحكم الإدارية - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request
from flask_login import login_required
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف الـ Blueprint
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.route('/admin/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    تحميل بيانات لوحة التحكم مع تحصين كامل ضد انهيار قاعدة البيانات
    """
    # قيم افتراضية لمنع انهيار الصفحة
    stats = {
        'total_suppliers': 0,
        'total_balance': "0.00",
        'pending_settlements': 0,
        'recent_activities': []
    }

    try:
        # 1. إحصائيات الموردين
        try:
            stats['total_suppliers'] = Supplier.query.count()
        except Exception as e:
            print(f"⚠️ Suppliers Query Warning: {e}")
        
        # 2. حساب الأرصدة (تحقق من وجود الأعمدة ديناميكياً)
        try:
            wallets = SupplierWallet.query.all()
            total_sar = sum([getattr(w, 'sar_total', 0) for w in wallets])
            total_yer = sum([getattr(w, 'yer_total', 0) for w in wallets])
            # معادلة تحويل بسيطة للأرصدة
            total_balance = total_sar + (total_yer / 3.75) if total_yer else total_sar
            stats['total_balance'] = f"{total_balance:,.2f}"
        except Exception as e:
            print(f"⚠️ Balance Calculation Warning: {e}")

        # 3. آخر 5 عمليات (ترتيب آمن)
        try:
            # استخدام id للترتيب إذا فشل created_at
            recent_activities = WalletTransaction.query.order_by(
                getattr(WalletTransaction, 'created_at', WalletTransaction.id).desc()
            ).limit(5).all()
            stats['recent_activities'] = recent_activities
        except Exception as e:
            print(f"⚠️ Activities Query Warning: {e}")
            stats['recent_activities'] = []
        
        # 4. التسويات المعلقة
        try:
            stats['pending_settlements'] = WalletTransaction.query.filter_by(status='معلقة').count()
        except Exception as e:
            print(f"⚠️ Settlements Query Warning: {e}")
            stats['pending_settlements'] = 0

        return render_template('admin/dashboard_content.html', **stats)
        
    except Exception as e:
        print(f"❌ Critical Dashboard Error: {str(e)}")
        # نرسل القيم الافتراضية حتى تظهر الصفحة ولا تظهر رسالة 500 للمستخدم
        return render_template('admin/dashboard_content.html', **stats)

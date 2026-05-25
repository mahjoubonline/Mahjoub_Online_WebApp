# coding: utf-8
from flask import Blueprint, render_template
from flask_login import login_required
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet # استيراد الموديل للحسابات الدقيقة

# تعريف الـ Blueprint الخاص بلوحة التحكم
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/admin/dashboard')
@login_required
def dashboard():
    try:
        # 1. جلب إحصائيات الموردين
        total_suppliers = Supplier.query.count()
        
        # 2. حساب الأرصدة بدقة من جدول المحافظ (الذي يحتوي على الأرصدة المتعددة)
        # ملاحظة: تم الانتقال لحساب الأرصدة من SupplierWallet وليس Supplier.balance
        wallets = SupplierWallet.query.all()
        total_sar_balance = sum([w.sar_total for w in wallets])
        total_yer_balance = sum([w.yer_total for w in wallets])
        
        # 3. جلب آخر 5 عمليات من جدول الحركات
        from apps.models.wallet_db import WalletTransaction
        recent_activities = WalletTransaction.query.order_by(WalletTransaction.created_at.desc()).limit(5).all()
        
        # 4. حساب التسويات المعلقة
        pending_settlements = WalletTransaction.query.filter_by(status='معلقة').count()

        # إرسال البيانات للواجهة
        return render_template(
            'admin/dashboard_content.html', # تم تصحيح المسار ليتطابق مع ملفك
            total_suppliers=total_suppliers,
            total_sar_balance=total_sar_balance,
            total_yer_balance=total_yer_balance,
            pending_settlements=pending_settlements,
            recent_activities=recent_activities
        )
        
    except Exception as e:
        # في حال حدوث خطأ، يطبع الخطأ في الـ Console ويمنع انهيار السيرفر
        print(f"Error loading dashboard: {e}")
        return "حدث خطأ أثناء تحميل لوحة التحكم، يرجى مراجعة سجلات النظام.", 500

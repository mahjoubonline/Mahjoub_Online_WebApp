# coding: utf-8
# 📊 لوحة التحكم الإدارية - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template
from flask_login import login_required
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف الـ Blueprint الخاص بلوحة التحكم
admin_dashboard = Blueprint('admin_dashboard', __name__)

@admin_dashboard.route('/admin/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    تحميل بيانات لوحة التحكم مع معالجة أعمدة قاعدة البيانات المشفرة
    """
    try:
        # 1. إحصائيات الموردين
        total_suppliers = Supplier.query.count()
        
        # 2. حساب الأرصدة 
        # تم استخدام الأعمدة التي تبدأ بـ (_) لتطابق الموديل المشفر
        wallets = SupplierWallet.query.all()
        
        # استخدام (w._sar_total) بدلاً من (w.sar_total) لتجنب خطأ الحقل غير الموجود
        total_sar_balance = sum([float(w._sar_total or 0) for w in wallets])
        total_yer_balance = sum([float(w._yer_total or 0) for w in wallets])
        
        # إجمالي الرصيد للعرض في القالب
        total_balance = total_sar_balance + (total_yer_balance / 3.75) 
        
        # 3. آخر 5 عمليات
        recent_activities = WalletTransaction.query.order_by(
            WalletTransaction.created_at.desc()
        ).limit(5).all()
        
        # 4. التسويات المعلقة
        pending_settlements = WalletTransaction.query.filter_by(status='معلقة').count()

        return render_template(
            'admin/dashboard_content.html',
            total_suppliers=total_suppliers,
            total_balance=f"{total_balance:,.2f}",
            pending_settlements=pending_settlements,
            recent_activities=recent_activities
        )
        
    except Exception as e:
        # تسجيل الخطأ في السجلات للتشخيص
        print(f"❌ Error loading dashboard: {str(e)}")
        
        # رسالة واجهة المستخدم في حال فشل تحميل البيانات
        return """
        <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
            <h2>حدث خطأ أثناء تحميل لوحة التحكم</h2>
            <p>يرجى التأكد من تحديث هيكل قاعدة البيانات (الأعمدة مفقودة).</p>
            <a href="/admin/dashboard" style="padding:10px; background:#632C8F; color:white; text-decoration:none; border-radius:5px;">حاول مجدداً</a>
        </div>
        """, 500

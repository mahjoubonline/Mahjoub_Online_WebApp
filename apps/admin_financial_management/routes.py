# coding: utf-8
# 📂 apps/admin_financial_management/routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required
from apps.extensions import db
from apps.models.wallet_db import WalletTransaction
from sqlalchemy import func

# تعريف البلوبرنت الخاص بإدارة المالية
financial_mgmt_bp = Blueprint(
    'financial_mgmt_bp', 
    __name__, 
    template_folder='templates'
)

@financial_mgmt_bp.route('/dashboard', methods=['GET'])
@login_required
def financial_dashboard():
    """لوحة التحكم المالية: تقرير الأرباح والخسائر ونظام الدائن والمدين."""
    
    # 1. حساب إجمالي الدائن (كل ما دخل كعمولات منصة أو إيرادات)
    total_credit = db.session.query(func.sum(WalletTransaction.amount))\
        .filter(WalletTransaction.trans_type.in_(['platform_commission', 'sale_revenue'])).scalar() or 0.00
    
    # 2. حساب إجمالي المدين (كل ما خرج كعمولات مسوقين أو تسويات)
    total_debit = db.session.query(func.sum(WalletTransaction.amount))\
        .filter(WalletTransaction.trans_type.in_(['marketer_commission', 'adjustment_debit'])).scalar() or 0.00
    
    # 3. صافي الربح للمنصة
    net_profit = total_credit - total_debit
    
    # 4. جلب أحدث 50 حركة مالية لعرضها في جدول الدائن والمدين
    transactions = WalletTransaction.query.order_by(WalletTransaction.created_at.desc()).limit(50).all()
    
    # 5. تجهيز البيانات للعرض
    processed_transactions = []
    for t in transactions:
        # تصنيف الحركة: هل هي دائنة أم مدينة؟
        is_credit = t.trans_type in ['platform_commission', 'sale_revenue', 'adjustment_credit']
        processed_transactions.append({
            'created_at': t.created_at,
            'description': t.description or t.trans_type,
            'related_order_id': getattr(t, 'order_id', 'N/A'),
            'debit': t.amount if not is_credit else 0.00,
            'credit': t.amount if is_credit else 0.00
        })

    return render_template(
        'admin_financial_management.html',
        total_credit=float(total_credit),
        total_debit=float(total_debit),
        net_profit=float(net_profit),
        transactions=processed_transactions
    )

def register_module(app):
    """تسجيل موديول الإدارة المالية في التطبيق."""
    app.register_blueprint(financial_mgmt_bp, url_prefix='/admin/financial-management')

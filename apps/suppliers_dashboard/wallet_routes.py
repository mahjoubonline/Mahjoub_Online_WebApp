# coding: utf-8
# 📂 apps/suppliers_dashboard/routes/wallet_routes.py

from flask import Blueprint, render_template, abort, session, request, flash, redirect, url_for
from flask_login import login_required, current_user

from apps.models import db, Supplier, SupplierWallet

# تعريف الـ Blueprint
wallet_bp = Blueprint(
    'suppliers_wallet',
    __name__,
    template_folder='templates'
)


def get_supplier_context():
    """دالة مساعدة لجلب المورد والمحفظة بأمان"""
    user_type = session.get('user_type')
    if user_type not in ['supplier', 'staff']:
        return None
        
    supplier_id = current_user.supplier_id if user_type == 'staff' else current_user.id
    supplier = db.session.get(Supplier, supplier_id)
    
    if supplier:
        wallet = db.session.execute(
            db.select(SupplierWallet).filter_by(supplier_id=supplier.id)
        ).unique().scalar_one_or_none()
        supplier.wallet = wallet
        
    return supplier


@wallet_bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    """صفحة السحب من المحفظة (عملة SAR فقط)"""
    supplier = get_supplier_context()
    if not supplier:
        return redirect('/supplier/login')
    
    wallet = supplier.wallet
    if not wallet:
        flash('❌ لا توجد محفظة مرتبطة بحسابك', 'danger')
        return redirect(url_for('suppliers_dashboard.dashboard'))
    
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            
            # التحقق من المبلغ
            if amount <= 0:
                flash('❌ المبلغ يجب أن يكون أكبر من صفر', 'danger')
                return redirect(url_for('suppliers_wallet.withdraw'))
            
            if amount < 10:
                flash('❌ الحد الأدنى للسحب هو 10 ريال سعودي', 'danger')
                return redirect(url_for('suppliers_wallet.withdraw'))
            
            if amount > wallet.balance_sar:
                flash(f'❌ الرصيد غير كافٍ. الرصيد الحالي: {wallet.balance_sar:.2f} SAR', 'danger')
                return redirect(url_for('suppliers_wallet.withdraw'))
            
            # ✅ تسجيل طلب السحب
            # هنا يمكن إضافة منطق إنشاء طلب سحب في جدول withdrawals
            
            flash(f'✅ تم تقديم طلب سحب بمبلغ {amount:.2f} SAR بنجاح', 'success')
            return redirect(url_for('suppliers_dashboard.dashboard'))
            
        except ValueError:
            flash('❌ قيمة المبلغ غير صحيحة', 'danger')
    
    return render_template('suppliers/withdraw.html', supplier=supplier, wallet=wallet)


@wallet_bp.route('/wallet', methods=['GET'])
@login_required
def wallet():
    """صفحة تفاصيل المحفظة"""
    supplier = get_supplier_context()
    if not supplier:
        return redirect('/supplier/login')
    
    wallet = supplier.wallet
    if not wallet:
        flash('❌ لا توجد محفظة مرتبطة بحسابك', 'danger')
        return redirect(url_for('suppliers_dashboard.dashboard'))
    
    # هنا يمكن جلب تاريخ المعاملات
    from apps.models.wallet_db import WalletTransaction
    transactions = WalletTransaction.query.filter_by(
        wallet_id=wallet.id
    ).order_by(WalletTransaction.created_at.desc()).limit(50).all()
    
    return render_template(
        'suppliers/wallet.html',
        supplier=supplier,
        wallet=wallet,
        transactions=transactions
    )

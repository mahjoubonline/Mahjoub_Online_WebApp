# coding: utf-8
# 🔑 محرك العمليات المالية والتحكم بالمحافظ - منصة محجوب أونلاين 2026

from flask import render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from apps import db
from apps.models.wallet_db import Wallet, WalletTransaction
from . import admin_wallet  # استيراد البلوبرينت الخاص بإدارة المحفظة
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func

@admin_wallet.route('/overview', methods=['GET'])
@login_required
def overview():
    """
    الواجهة السيادية الموحدة لإدارة وحوكمة المحافظ المالية للإدارة العليا.
    تم تحصينها بالكامل باستخدام func.coalesce لمنع الأخطاء في حال كانت الجداول فارغة.
    """
    try:
        # 1. احتساب المؤشرات المالية الكلية للمنصة (الريال اليمني) مع معالجة القيم الفارغة
        yer_totals = db.session.query(
            func.coalesce(func.sum(Wallet.yer_total), 0.0),
            func.coalesce(func.sum(Wallet.yer_available), 0.0),
            func.coalesce(func.sum(Wallet.yer_pending), 0.0)
        ).first()

        # 2. احتساب المؤشرات المالية الكلية للمنصة (الريال السعودي) مع معالجة القيم الفارغة
        sar_totals = db.session.query(
            func.coalesce(func.sum(Wallet.sar_total), 0.0),
            func.coalesce(func.sum(Wallet.sar_available), 0.0),
            func.coalesce(func.sum(Wallet.sar_pending), 0.0)
        ).first()

        # 3. احتساب المؤشرات المالية الكلية للمنصة (الدولار الأمريكي) مع معالجة القيم الفارغة
        usd_totals = db.session.query(
            func.coalesce(func.sum(Wallet.usd_total), 0.0),
            func.coalesce(func.sum(Wallet.usd_available), 0.0),
            func.coalesce(func.sum(Wallet.usd_pending), 0.0)
        ).first()

        # 4. جلب طلبات السحب المعلقة (Pending) بأمان مع تحميل بيانات المورد لتجنب استعلامات Lazy Loading منفصلة
        pending_withdrawals = db.session.query(WalletTransaction)\
            .options(joinedload(WalletTransaction.wallet).joinedload(Wallet.supplier))\
            .filter(WalletTransaction.tx_type == 'withdrawal', WalletTransaction.tx_status == 'pending')\
            .order_by(WalletTransaction.created_at.desc())\
            .all()

        # تجميع المؤشرات المالية في قاموس منظم ومضمون القيمة لمنع أخطاء جينجا القاتلة
        platform_metrics = {
            "YER": {"total": yer_totals[0] or 0.0, "available": yer_totals[1] or 0.0, "pending": yer_totals[2] or 0.0},
            "SAR": {"total": sar_totals[0] or 0.0, "available": sar_totals[1] or 0.0, "pending": sar_totals[2] or 0.0},
            "USD": {"total": usd_totals[0] or 0.0, "available": usd_totals[1] or 0.0, "pending": usd_totals[2] or 0.0}
        }

        return render_template(
            'admin/overview.html',
            metrics=platform_metrics,
            pending_tx=pending_withdrawals,
            owner=current_user
        )

    except Exception as e:
        current_app.logger.error(f"❌ خطأ حوكمي أثناء تشغيل واجهة المحافظ: {str(e)}")
        return f"<h3>خطأ مالي في السيرفر الداخلي للعملات:</h3> <p>{str(e)}</p>", 500


@admin_wallet.route('/approve-withdrawal', methods=['POST'])
@login_required
def approve_withdrawal():
    """
    محرك التعميد المالي السيادي: الموافقة على طلب السحب وتحويل الأموال للمورد.
    """
    tx_id = request.form.get('tx_id')
    if not tx_id:
        return jsonify({"status": "error", "message": "المعرف الفريد للعملية مفقود."}), 400

    try:
        # استخدام with_for_update لمنع الـ Race Condition وتضارب البيانات على السيرفر الحي
        transaction = WalletTransaction.query.with_for_update().get(tx_id)
        
        if not transaction or transaction.tx_status != 'pending':
            return jsonify({"status": "error", "message": "العملية غير موجودة أو تم تعميدها مسبقاً."}), 400

        wallet = Wallet.query.with_for_update().get(transaction.wallet_id)
        currency = transaction.currency
        amount = transaction.amount

        # الخصم المالي الحوكمي حسب نوع عملة الحوالة المبرمة في الطلب وتعديل الأرصدة الإجمالية
        if currency == 'YER':
            if wallet.yer_pending < amount:
                return jsonify({"status": "error", "message": "رصيد الريال اليمني المعلق غير كافٍ لإتمام العملية."}), 400
            wallet.yer_pending -= amount
            wallet.yer_total -= amount
            wallet.yer_withdrawn += amount
            
        elif currency == 'SAR':
            if wallet.sar_pending < amount:
                return jsonify({"status": "error", "message": "رصيد الريال السعودي المعلق غير كافٍ لإتمام العملية."}), 400
            wallet.sar_pending -= amount
            wallet.sar_total -= amount
            wallet.sar_withdrawn += amount
            
        elif currency == 'USD':
            if wallet.usd_pending < amount:
                return jsonify({"status": "error", "message": "رصيد الدولار المعلق غير كافٍ لإتمام العملية."}), 400
            wallet.usd_pending -= amount
            wallet.usd_total -= amount
            wallet.usd_withdrawn += amount

        # تحديث حالة السجل المالي وتوثيق هوية المسؤول المعمّد للمشهد
        transaction.tx_status = 'completed'
        transaction.approved_by_id = current_user.id if hasattr(current_user, 'id') else None
        
        db.session.commit()
        return jsonify({"status": "success", "message": f"تم تعميد صرف الحوالة بنجاح برقم المرجع: {transaction.transaction_ref}"}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ خطر مالي أثناء تعميد السحب: {str(e)}")
        return jsonify({"status": "error", "message": f"فشل التعميد المالي: {str(e)}"}), 500


@admin_wallet.route('/reject-withdrawal', methods=['POST'])
@login_required
def reject_withdrawal():
    """
    رفض طلب السحب سيادياً: إعادة الأموال المحتجزة من الرصيد المعلق (Pending) إلى رصيد المورد المتاح (Available).
    """
    tx_id = request.form.get('tx_id')
    reason = request.form.get('reason', 'تم الرفض من قبل الإدارة العليا').strip()

    if not tx_id:
        return jsonify({"status": "error", "message": "المعرف الفريد للعملية مفقود."}), 400

    try:
        transaction = WalletTransaction.query.with_for_update().get(tx_id)
        if not transaction or transaction.tx_status != 'pending':
            return jsonify({"status": "error", "message": "العملية غير صالحة لإجراء الرفض."}), 400

        wallet = Wallet.query.with_for_update().get(transaction.wallet_id)
        currency = transaction.currency
        amount = transaction.amount

        # الحوكمة المحاسبية: إعادة المال من المعلق (Pending) إلى المتاح (Available) لأن العملية رُفضت ولم تُصرف
        if currency == 'YER':
            wallet.yer_pending -= amount
            wallet.yer_available += amount
        elif currency == 'SAR':
            wallet.sar_pending -= amount
            wallet.sar_available += amount
        elif currency == 'USD':
            wallet.usd_pending -= amount
            wallet.usd_available += amount

        # إسقاط وتغيير حالة العملية المادية إلى مرفوضة وتوثيق مبرر الرفض
        transaction.tx_status = 'rejected'
        transaction.description = f"{transaction.description} | سبب الرفض الحوكمي: {reason}"
        transaction.approved_by_id = current_user.id if hasattr(current_user, 'id') else None
        
        db.session.commit()
        return jsonify({"status": "success", "message": "تم رفض طلب السحب بنجاح وإعادة فك حجز الأموال إلى رصيد التاجر المتاح."}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ خطأ أثناء إسقاط العملية المالية: {str(e)}")
        return jsonify({"status": "error", "message": f"فشل إجراء إسقاط الحوالة: {str(e)}"}), 500

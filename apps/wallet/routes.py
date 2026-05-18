# coding: utf-8
# 💳 محرك الحوكمة المالية والمسارات السيادية للمحافظ - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from apps import db
from apps.models.supplier_db import Supplier

# 🛡️ استدعاء آمن ومحصن للموديلات لمنع الانهيار الكلي للسيرفر (Crash-Proof)
try:
    from apps.models.wallet_db import Wallet
except ImportError:
    # إذا فشل الاستدعاء لأي سبب، يتم بناء كلاس وهمي لمنع انهيار إقلاع الفلاسك
    class Wallet(object):
        query = None

# محاولة جلب جدول الحركات بشكل ديناميكي مرن
WalletTransaction = None
try:
    import apps.models.wallet_db as w_model
    if hasattr(w_model, 'WalletTransaction'):
        WalletTransaction = getattr(w_model, 'WalletTransaction')
    elif hasattr(w_model, 'WalletTransactions'):
        WalletTransaction = getattr(w_model, 'WalletTransactions')
except Exception:
    pass

# إنشاء البلوبرينت المالي
admin_wallet = Blueprint('admin_wallet', __name__, template_folder='templates')

@admin_wallet.route('/admin/wallet/overview', methods=['GET'])
@login_required
def overview():
    """
    شاشة فحص وجرد الحسابات المادية مع التفتيش الفوري
    """
    if current_user.role not in ['Owner', 'Admin']:
        flash('غير مسموح لك بامتلاك صلاحية دخول الفضاء المالي.', 'danger')
        return redirect(url_for('admin_dashboard.dashboard_home'))

    search_query = request.args.get('search', '').strip()
    wallets = []
    
    if Wallet.query is None:
        flash('تنبيه: قاعدة بيانات المحافظ غير متصلة بالنواة بشكل صحيح حالياً.', 'warning')
        return render_template('admin/overview.html', wallets=wallets)

    try:
        # بناء استعلام جلب الحسابات مع ربط الموردين
        query = Wallet.query.join(Supplier, Wallet.supplier_id == Supplier.id)

        if search_query and search_query != '#':
            query = query.filter(
                (Supplier.trade_name.like(f'%{search_query}%')) |
                (Supplier.sovereign_id.like(f'%{search_query}%')) |
                (Wallet.wallet_code.like(f'%{search_query}%'))
            )

        wallets = query.all()
    except Exception as e:
        print(f"📡 تنبيه حوكمة المحافظ: جاري مواءمة الجداول الهيكلية: {e}")

    return render_template('admin/overview.html', wallets=wallets)


@admin_wallet.route('/api/wallet/<string:wallet_code>/balance', methods=['GET'])
@login_required
def get_wallet_balance_api(wallet_code):
    """
    واجهة برمجة تطبيقات (API) آمنة بنظام JSON لخدمة العمليات البرمجية في اللوحات الأخرى
    """
    if current_user.role not in ['Owner', 'Admin']:
        return jsonify({"status": "error", "message": "صلاحية سيادية مرفوضة"}), 403

    if Wallet.query is None:
        return jsonify({"status": "error", "message": "قاعدة البيانات غير متصلة"}), 500

    wallet = Wallet.query.filter_by(wallet_code=wallet_code).first()
    if not wallet:
        return jsonify({"status": "error", "message": "المحفظة المالية غير موجودة بالنظام"}), 404

    wallet_data = {
        "id": wallet.id,
        "wallet_code": wallet.wallet_code,
        "yer_balance": getattr(wallet, 'yer_balance', 0.0),
        "sar_balance": getattr(wallet, 'sar_balance', 0.0),
        "usd_balance": getattr(wallet, 'usd_balance', 0.0)
    }

    return jsonify({"status": "success", "data": wallet_data})


@admin_wallet.route('/admin/wallet/adjust', methods=['POST'])
@login_required
def adjust_balance():
    """
    سلطة الضبط المباشر للمالك لتعديل وحفظ الأرصدة الثلاثية
    """
    if current_user.role != 'Owner':
        flash('هذا الإجراء يتطلب سلطة المالك السيادية المطلقة.', 'danger')
        return redirect(url_for('admin_wallet.overview'))

    wallet_id = request.form.get('wallet_id')
    currency = request.form.get('currency')  
    action_type = request.form.get('action_type')  
    amount_str = request.form.get('amount', '0')

    if Wallet.query is None:
        flash('النظام متاح للقراءة فقط حالياً لعدم اكتمال الربط.', 'danger')
        return redirect(url_for('admin_wallet.overview'))

    try:
        amount = float(amount_str)
        if amount <= 0:
            flash('يجب أن تكون القيمة المالية أكبر من صفر.', 'warning')
            return redirect(url_for('admin_wallet.overview'))
            
        wallet = Wallet.query.get(wallet_id)
        if not wallet:
            flash('المحفظة المستهدفة غير مسجلة.', 'danger')
            return redirect(url_for('admin_wallet.overview'))

        # التعديل المباشر والآمن للأرصدة عبر الـ Dynamic Fallback الحامي للحقول
        if currency == 'YER':
            current_bal = float(getattr(wallet, 'yer_balance', 0.0))
            wallet.yer_balance = (current_bal + amount) if action_type == 'deposit' else (current_bal - amount)

        elif currency == 'SAR':
            current_bal = float(getattr(wallet, 'sar_balance', 0.0))
            wallet.sar_balance = (current_bal + amount) if action_type == 'deposit' else (current_bal - amount)

        elif currency == 'USD':
            current_bal = float(getattr(wallet, 'usd_balance', 0.0))
            wallet.usd_balance = (current_bal + amount) if action_type == 'deposit' else (current_bal - amount)
        
        # محاولة توثيق الحركة في السجلات المادية إذا كان الجدول متاحاً
        if WalletTransaction is not None:
            try:
                tx_log = WalletTransaction(
                    wallet_id=wallet.id,
                    transaction_type=action_type,
                    currency=currency,
                    amount=amount,
                    description="تعديل إداري مباشر من لوحة تحكم المالك السيادية"
                )
                db.session.add(tx_log)
            except Exception as tx_err:
                print(f"⚠️ تخطي حفظ وثيقة التحويل: {tx_err}")
        else:
            print(f"📝 [سجل النظام الحركي]: تم {action_type} بمبلغ {amount} {currency} للمحفظة {wallet.wallet_code}")

        db.session.commit()
        flash(f'تم تحديث كشف حساب المحفظة {wallet.wallet_code} بنجاح وتصفير التعارضات.', 'success')

    except ValueError:
        flash('خطأ: صيغة المبلغ المدخل غير صالحة.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'تعذر تعديل الرصيد بسبب عطل في الربط الهيكلي: {e}', 'danger')

    return redirect(url_for('admin_wallet.overview'))

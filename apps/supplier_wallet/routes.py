# coding: utf-8
# 📂 apps/supplier_wallet/routes.py

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
# استيراد الخدمة مباشرة لتجنب الاستيراد الدائري
from apps.supplier_wallet.services import WalletService

# تعريف الـ Blueprint الخاص بالمورد
supplier_wallet_bp = Blueprint(
    'supplier_wallet', 
    __name__, 
    template_folder='templates'
)

@supplier_wallet_bp.route('/my-wallet', methods=['GET'])
@login_required
def view_my_wallet():
    """
    عرض خزانة المورد الخاصة بالمستخدم المسجل حالياً.
    نعتمد هنا على العلاقة المباشرة بين المورد والمحفظة.
    """
    # 1. جلب المحفظة من خلال العلاقة المعرفة في الموديل
    wallet = getattr(current_user, 'wallet', None)
    
    # 2. إذا لم يجد علاقة مباشرة، نحاول جلبها عبر الخدمة كإجراء احتياطي
    if not wallet:
        wallet = WalletService.get_supplier_wallet(current_user.id)
    
    # 3. التحقق من وجود المحفظة
    if not wallet:
        abort(404, description="لم يتم العثور على محفظة مرتبطة بحسابك.")

    # 4. عرض القالب مع تمرير كائن المحفظة
    # ملاحظة: كائن wallet يحتوي الآن على transactions مرتبة عبر القالب
    return render_template('supplier_wallet/supplier_wallet.html', wallet=wallet)

# ملاحظة: النظام يعتمد الآن على العلاقات المباشرة (Relationships) في SQLAlchemy،
# مما يضمن دقة البيانات وسرعة الاستعلام.

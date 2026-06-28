# coding: utf-8
# 📂 apps/supplier_wallet/routes.py

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
# استيراد الخدمة مباشرة لتجنب الاستيراد الدائري (Circular Import)
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
    # استخدام العلاقة 'wallet' المعرفة في موديل Supplier
    # هذا يغنينا عن البحث عن supplier_id يدوياً
    wallet = current_user.wallet
    
    # إذا لم يجد علاقة مباشرة، نحاول جلبها باستخدام معرف المورد (احتياطاً)
    if not wallet:
        wallet = WalletService.get_supplier_wallet(current_user.id)
    
    if not wallet:
        # إذا لم تكن المحفظة موجودة، نرجع خطأ 404
        abort(404, description="لم يتم العثور على محفظة مرتبطة بحسابك.")

    # عرض القالب مع تمرير كائن المحفظة
    return render_template('supplier_wallet/supplier_wallet.html', wallet=wallet)

# ملاحظة: تم تعديل المنطق ليعتمد على current_user.wallet 
# الذي يربط المورد بمحفظته تلقائياً عبر SQLAlchemy.

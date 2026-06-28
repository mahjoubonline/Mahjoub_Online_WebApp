# coding: utf-8
# 📂 apps/supplier_wallet/routes.py

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
# استيراد الخدمة مباشرة لتجنب الاستيراد الدائري (Circular Import)
from apps.supplier_wallet.services import WalletService

# تعريف الـ Blueprint الخاص بالمورد
# الربط يتم عبر registry.py باستخدام الاسم 'supplier_wallet'
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
    نستخدم معرف المورد من current_user لضمان الخصوصية التامة.
    """
    # جلب معرف المورد من المستخدم الحالي
    # تأكد أن كائن الـ current_user يحتوي على خاصية supplier_id
    supplier_id = getattr(current_user, 'supplier_id', None)
    
    if not supplier_id:
        # إيقاف الوصول إذا كان المستخدم لا يملك صلاحية المورد
        abort(403, description="عذراً، لا تملك صلاحية الوصول إلى هذه الخزانة.")

    # جلب بيانات المحفظة من خلال خدمة المورد
    wallet = WalletService.get_supplier_wallet(supplier_id)
    
    if not wallet:
        # في حال لم يتم العثور على محفظة مرتبطة بحساب المورد
        abort(404, description="لم يتم العثور على محفظة مرتبطة بحسابك.")

    # عرض القالب مع تمرير كائن المحفظة
    return render_template('supplier_wallet/supplier_wallet.html', wallet=wallet)

# ملاحظة: يمكنك إضافة مسارات أخرى هنا (مثل طلب سحب رصيد) 
# واستخدام WalletService.process_transaction للعمليات المالية.

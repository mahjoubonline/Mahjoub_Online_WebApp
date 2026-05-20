# coding: utf-8
# 🏦 محرك الفضاء المالي - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template
from flask_login import login_required
from apps import db

# تعريف البلوبرينت باسم 'admin_wallet' كما تم تسجيله في المصنع المركزي
admin_wallet = Blueprint(
    'admin_wallet', 
    __name__, 
    template_folder='templates'
)

@admin_wallet.route('/overview', methods=['GET'])
@login_required
def wallet_page():
    """
    عرض لوحة التحكم الخاصة بالمحفظة (حوكمة وفحص المحافظ).
    تم تغيير اسم الدالة من wallet_overview إلى wallet_page 
    لتتطابق مع المسار الذي يبحث عنه النظام.
    """
    try:
        # هنا سيتم جلب بيانات المحافظ من قاعدة البيانات لاحقاً
        return render_template('admin/wallet.html')
    except Exception as e:
        return f"خطأ في بوابة الفضاء المالي: {str(e)}", 500

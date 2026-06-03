# 📂 apps/admin_dashboard/routes.py (النسخة المصححة)

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from apps.extensions import db 
from sqlalchemy import func

# ✅ التصحيح: إزالة url_prefix من هنا لأنك قمت بتعريفه في __init__.py
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # ... (بقية الكود الخاص بك كما هو) ...
    from apps.models.supplier_db import Supplier
    from apps.models.wallet_db import SupplierWallet, WalletTransaction
    
    # ... (الكود المتبقي) ...
    return render_template('admin/dashboard_content.html', **stats)

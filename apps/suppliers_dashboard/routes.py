# coding: utf-8
from flask import Blueprint, render_template, abort, session
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier

# 1. هذا الـ Blueprint مخصص للداشبورد فقط
suppliers_dashboard_bp = Blueprint('suppliers_dashboard', __name__, template_folder='templates')

@suppliers_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # التحقق من أن المستخدم مورد (أو موظف)
    if 'user_type' not in session:
        abort(403)
        
    # جلب بيانات المورد بناءً على ID المستخدم الحالي
    supplier = Supplier.query.get(current_user.id)
    
    # عرض صفحة الداشبورد
    return render_template('suppliers/dashboard.html', supplier=supplier)

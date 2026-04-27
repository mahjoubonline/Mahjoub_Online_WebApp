from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import admin_bp
from core.models import User, db

# --- حماية القيادة العليا ---
def admin_only(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("⚠️ هذا النطاق مخصص للقيادة العليا فقط.", "error")
            return redirect(url_for('supplier_panel.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# --- لوحة التحكم الرئيسية للإدارة ---
@admin_bp.route('/dashboard')
@login_required
@admin_only
def dashboard():
    # جلب قائمة الموردين الذين ينتظرون التعميد
    pending_suppliers = User.query.filter_by(role='supplier', status='pending').all()
    # جلب إحصائيات سريعة
    stats = {
        'total_users': User.query.count(),
        'pending_count': len(pending_suppliers)
    }
    return render_template('admin_panel/dashboard.html', suppliers=pending_suppliers, stats=stats)

# --- محرك التعميد (Approve) ---
@admin_bp.route('/approve/<int:user_id>')
@login_required
@admin_only
def approve_supplier(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'approved'
    db.session.commit()
    flash(f"✅ تم تعميد الشريك {user.name}، يمكنه الآن دخول الترسانة.", "success")
    return redirect(url_for('admin_panel.dashboard'))

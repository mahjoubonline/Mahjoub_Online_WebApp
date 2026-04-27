from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import admin_bp
from core.models import User, db

# حماية سيادية: التأكد أن الداخل هو المدير فقط
def admin_required(f):
    def wrap(*args, **kwargs):
        if current_user.role != 'admin':
            flash("⚠️ غير مسموح بالدخول لغير القيادة العليا.", "error")
            return redirect(url_for('supplier_panel.login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # إحصائيات سريعة للقيادة
    total_suppliers = User.query.filter_by(role='supplier').count()
    pending_suppliers = User.query.filter_by(role='supplier', status='pending').count()
    return render_template('admin_panel/dashboard.html', 
                           total=total_suppliers, 
                           pending=pending_suppliers)

@admin_bp.route('/approve-supplier/<int:user_id>')
@login_required
@admin_required
def approve_supplier(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'approved'
    db.session.commit()
    flash(f"✅ تم تعميد الشريك {user.name} بنجاح.", "success")
    return redirect(url_for('admin_panel.dashboard'))

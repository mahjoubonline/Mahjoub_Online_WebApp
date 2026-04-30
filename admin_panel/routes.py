from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from core.models import User, Supplier, Product, db  # استيراد موحد من الترسانة

# تعريف البلوبرنت الخاص بالإدارة المركزية
admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')

@admin_panel.route('/dashboard')
@login_required
def dashboard():
    # حماية سيادية: التأكد من أن المستخدم هو الأدمن فقط
    if current_user.role != 'admin':
        flash('دخول غير مصرح! هذه المنطقة تخضع للرقابة الإدارية.', 'danger')
        return redirect(url_for('supplier_panel.dashboard'))

    # إحصائيات سريعة للمنصة (PageSpeed Optimized)
    stats = {
        'total_suppliers': Supplier.query.count(),
        'total_products': Product.query.count(),
        'pending_verifications': Supplier.query.filter_by(is_verified=False).count()
    }
    
    return render_template('admin_panel/dashboard.html', stats=stats)

@admin_panel.route('/manage-suppliers')
@login_required
def manage_suppliers():
    if current_user.role != 'admin':
        return redirect(url_for('supplier_panel.dashboard'))
        
    # جلب جميع الموردين المسجلين في النظام
    all_suppliers = Supplier.query.all()
    return render_template('admin_panel/manage_suppliers.html', suppliers=all_suppliers)

@admin_panel.route('/verify-supplier/<int:supplier_id>')
@login_required
def verify_supplier(supplier_id):
    if current_user.role != 'admin':
        return redirect(url_for('supplier_panel.dashboard'))
    
    supplier = Supplier.query.get_or_404(supplier_id)
    supplier.is_verified = True
    db.session.commit()
    flash(f'تم اعتماد المتجر: {supplier.store_name} بنجاح.', 'success')
    return redirect(url_for('admin_panel.manage_suppliers'))

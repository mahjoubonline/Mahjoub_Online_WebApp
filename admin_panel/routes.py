from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from core import db
import os

# 1. إعداد المسار والـ Blueprint
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
admin_bp = Blueprint('admin_panel', __name__, template_folder=template_dir)

# --- معالج السياق لإظهار التنبيهات في الشريط الجانبي ---
@admin_bp.context_processor
def inject_counts():
    from core.models import Supplier
    try:
        pending_count = Supplier.query.filter_by(is_approved=False).count()
        return dict(pending_suppliers_count=pending_count)
    except:
        return dict(pending_suppliers_count=0)

# 2. لوحة التحكم (الرئيسية)
@admin_bp.route('/', strict_slashes=False)
@login_required
def dashboard():
    from core.models import Supplier, Product
    try:
        s_count = Supplier.query.count()
        p_count = Product.query.count()
        # جلب أحدث الموردين للعرض السريع في الواجهة
        latest_suppliers = Supplier.query.order_by(Supplier.created_at.desc()).limit(5).all()
        return render_template('dashboard.html', s_count=s_count, p_count=p_count, latest_suppliers=latest_suppliers)
    except Exception as e:
        print(f"⚠️ خطأ في الإحصائيات: {e}")
        return render_template('dashboard.html', s_count=0, p_count=0)

# 3. إدارة الموردين (الربط الحقيقي مع القالب)
@admin_bp.route('/suppliers/management', strict_slashes=False)
@login_required
def manage_suppliers():
    from core.models import Supplier
    # جلب جميع الموردين لعرضهم في جدول الإدارة الذي صممناه
    all_suppliers = Supplier.query.order_by(Supplier.created_at.desc()).all()
    return render_template('admin_suppliers_management.html', suppliers=all_suppliers)

# 4. تنفيذ أمر الاعتماد السيادي
@admin_bp.route('/suppliers/approve/<int:supplier_id>')
@login_required
def approve_supplier(supplier_id):
    from core.models import Supplier
    supplier = Supplier.query.get_or_404(supplier_id)
    
    try:
        supplier.is_approved = True
        db.session.commit()
        flash(f'✅ تم منح الاعتماد السيادي للمورد: {supplier.username}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ عطل في القاعدة: {str(e)}', 'danger')
        
    return redirect(url_for('admin_panel.manage_suppliers'))

# 5. بوابة الولوج السيادي (مع حماية الفصل)
@admin_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        from core.models import User
        user = User.query.filter_by(username=username).first()

        if user and user.password == password: 
            # قفل الأمان: نحدد أن الداخل هو أدمن قبل تسجيل الدخول
            session['user_type'] = 'admin'
            login_user(user)
            flash('أهلاً بك أيها القائد في برج الرقابة', 'success')
            return redirect(url_for('admin_panel.dashboard'))
        else:
            flash('عذراً، بيانات الولوج السيادية غير صحيحة', 'danger')
            
    return render_template('login.html')

# 6. المزامنة والخروج
@admin_bp.route('/sync_now', strict_slashes=False)
@login_required
def sync_now():
    try:
        from core.qumra_sync import qumra_manager
        live_products = qumra_manager.fetch_live_products(limit=15)
        return render_template('product_review.html', products=live_products)
    except:
        return render_template('product_review.html', products=[])

@admin_bp.route('/logout')
@login_required
def logout():
    session.pop('user_type', None) # تنظيف الجلسة
    logout_user()
    flash('تم تأمين النظام وتسجيل الخروج بنجاح', 'info')
    return redirect(url_for('admin_panel.login'))

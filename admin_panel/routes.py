from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import os

# 1. إعداد مسار القوالب
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
admin_bp = Blueprint('admin_panel', __name__, template_folder=template_dir)

# 2. لوحة التحكم (محمية بـ @login_required)
@admin_bp.route('/', strict_slashes=False)
@login_required
def dashboard():
    from core.models import Supplier, Product
    try:
        s_count = Supplier.query.count()
        p_count = Product.query.count()
        return render_template('dashboard.html', s_count=s_count, p_count=p_count)
    except Exception as e:
        print(f"⚠️ خطأ في الإحصائيات: {e}")
        return render_template('dashboard.html', s_count=0, p_count=0)

# 3. بوابة الولوج السيادي (برج الرقابة المركزية)
@admin_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    # إذا كان القائد مسجلاً دخوله بالفعل، يذهب للداشبورد مباشرة
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        from core.models import User
        # البحث عن القائد في قاعدة البيانات
        user = User.query.filter_by(username=username).first()

        # التحقق من الهوية (ملاحظة: يفضل استخدام werkzeug.security لاحقاً لتشفير الباسورد)
        if user and user.password == password:
            login_user(user) # تثبيت الجلسة أمنياً
            flash('أهلاً بك أيها القائد في برج الرقابة', 'success')
            return redirect(url_for('admin_panel.dashboard'))
        else:
            flash('عذراً، بيانات الولوج السيادية غير صحيحة', 'danger')
            
    return render_template('login.html')

# 4. المزامنة (محمية أيضاً)
@admin_bp.route('/sync_now', strict_slashes=False)
@login_required
def sync_now():
    try:
        from core.qumra_sync import qumra_manager
        live_products = qumra_manager.fetch_live_products(limit=15)
        return render_template('product_review.html', products=live_products)
    except Exception:
        return render_template('product_review.html', products=[])

# 5. تسجيل الخروج وتأمين البرج
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تأمين النظام وتسجيل الخروج بنجاح', 'info')
    return redirect(url_for('admin_panel.login'))

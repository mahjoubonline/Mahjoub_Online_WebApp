from flask import Blueprint, render_template, request, redirect, url_for, flash
import os

# 1. تعريف البلوبرنت وتحديد مسار المجلد المطلق للقوالب لضمان عدم ظهور TemplateNotFound
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
admin_bp = Blueprint('admin_panel', __name__, template_folder=template_dir)

# 2. مسار لوحة التحكم الرئيسية (Dashboard)
@admin_bp.route('/', strict_slashes=False)
def dashboard():
    # استيراد متأخر لكسر الحلقة الدائرية
    from core.models import Supplier, Product
    try:
        s_count = Supplier.query.count()
        p_count = Product.query.count()
        return render_template('dashboard.html', s_count=s_count, p_count=p_count)
    except Exception as e:
        print(f"⚠️ تنبيه إحصائيات: {e}")
        return render_template('dashboard.html', s_count=0, p_count=0)

# 3. مسار تسجيل الدخول (بوابة برج الرقابة المركزية)
@admin_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        # استقبال البيانات من التصميم الذي جهزناه
        username = request.form.get('username')
        password = request.form.get('password')

        # التحقق من "كلمة المرور السيادية"
        # ملاحظة: سنقوم لاحقاً بربطها ببيانات قاعدة البيانات المشفرة
        if username == 'علي محجوب' and password == '123456': # يمكنك تغيير كلمة المرور هنا مؤقتاً
            flash('تم التحقق من الهوية.. أهلاً بك أيها القائد', 'success')
            return redirect(url_for('admin_panel.dashboard'))
        else:
            # إرسال رسالة خطأ تظهر في قسم flash-messages بالتصميم
            flash('عذراً، بيانات الولوج السيادية غير صحيحة', 'danger')
            return redirect(url_for('admin_panel.login'))

    # عرض صفحة HTML التي أرسلتها (تأكد أن اسمها login.html)
    return render_template('login.html')

# 4. مسار المزامنة وعرض المنتجات اللحظي
@admin_bp.route('/sync_now', strict_slashes=False)
def sync_now():
    try:
        from core.qumra_sync import qumra_manager
        live_products = qumra_manager.fetch_live_products(limit=15)
        return render_template('product_review.html', products=live_products)
    except Exception as e:
        print(f"❌ خطأ مزامنة: {e}")
        return render_template('product_review.html', products=[])

# 5. مسار تسجيل الخروج
@admin_bp.route('/logout')
def logout():
    flash('تم إنهاء الجلسة وتأمين البرج بنجاح', 'info')
    return redirect(url_for('admin_panel.login'))

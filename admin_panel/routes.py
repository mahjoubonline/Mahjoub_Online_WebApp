from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from core.models.user import User  # استيراد الموديل من قلب النظام

# 1. تعريف البلوبرينت
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

# ==========================================
# 1. بوابة الدخول السيادية (login.html)
# ==========================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    # إذا كان مسجلاً كأدمن بالفعل، يدخل فوراً
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin_panel.admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username') # تغيير من email إلى username
        password = request.form.get('password')
        
        # التحقق من الهوية الملكية (علي محجوب | 123)
        if username == "علي محجوب" and password == "123":
            user = User.query.filter_by(username="علي محجوب", role='admin').first()
            if user:
                login_user(user)
                return redirect(url_for('admin_panel.admin_dashboard'))
        
        # الرسالة المطلوبة في حال عدم التسجيل أو الخطأ
        flash('عذراً يا قائد، أنت غير مسجل في المنصة اللامركزية للإدارة.', 'danger')
            
    return render_template('admin_panel/login.html')

# ==========================================
# 2. لوحة التحكم المركزية (dashboard.html)
# ==========================================
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_panel/dashboard.html')

# ==========================================
# 3. إدارة الموردين (admin_suppliers_management.html)
# ==========================================
@admin_bp.route('/suppliers')
@login_required
def admin_suppliers_management():
    return render_template('admin_panel/admin_suppliers_management.html')

# ==========================================
# 4. المركز المالي (wallets.html)
# ==========================================
@admin_bp.route('/wallets')
@login_required
def wallets():
    return render_template('admin_panel/wallets.html')

# ==========================================
# 5. مراجعة المنتجات (product_review.html)
# ==========================================
@admin_bp.route('/reviews')
@login_required
def product_review():
    return render_template('admin_panel/product_review.html')

# ==========================================
# 6. تفاصيل المنتج (product_detail.html)
# ==========================================
@admin_bp.route('/product/<int:id>')
@login_required
def product_detail(id):
    return render_template('admin_panel/product_detail.html')

# ==========================================
# 7. تسجيل الخروج
# ==========================================
@admin_bp.route('/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_panel.admin_login'))

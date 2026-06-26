# أضف هذه الاستيرادات في الأعلى
from apps.models.admin_db import AdminUser
from apps.models.supplier_staff_db import SupplierStaff

@auth_portal.route(LOGIN_PATH, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # توجيه ذكي حسب الرتبة
        if hasattr(current_user, 'is_admin') and current_user.is_admin:
            return redirect(url_for('admin_dashboard.dashboard'))
        return redirect(url_for('suppliers_dashboard.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1. حاول التحقق كمسؤول
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('admin_dashboard.dashboard'))
            
        # 2. حاول التحقق كمورد
        user = SupplierStaff.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('suppliers_dashboard.dashboard'))
            
        flash('اسم المستخدم أو كلمة المرور غير صحيحة.', 'danger')
        
    return render_template('auth/login.html')

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # عند نجاح التحقق
        if username == 'ali_mahjoub' and password == 'الملك_2026':
            session['is_authenticated'] = True  # وضع ختم الدخول في الجلسة
            session['user_id'] = 'founder_ali'
            return redirect(url_for('admin.dashboard'))
        else:
            flash('تنبيه: بيانات الدخول غير صحيحة.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear() # مسح الجلسة تماماً عند الخروج لضمان عدم العودة للوراء
    return redirect(url_for('auth.login'))

from flask import Blueprint, render_template, session, redirect, url_for

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/dashboard')
def dashboard():
    # منع الدخول التلقائي: إذا لم يكن هناك ختم دخول، اطرده للبوابة
    if not session.get('is_authenticated'):
        return redirect(url_for('auth.login'))
    
    return render_template('admin/dashboard_content.html')

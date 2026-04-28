from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def supplier_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # التأكد أن المستخدم مورد ومعتمد
        if not current_user.is_authenticated or current_user.role != 'supplier':
            return redirect(url_for('supplier_panel.login'))
        if current_user.status != 'approved':
            return redirect(url_for('supplier_panel.waiting_approval'))
        return f(*args, **kwargs)
    return decorated_function

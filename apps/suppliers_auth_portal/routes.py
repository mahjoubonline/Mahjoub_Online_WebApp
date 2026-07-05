# coding: utf-8
# 📂 apps/suppliers_auth_portal/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
from apps.models.supplier_db import Supplier
from apps.models.marketer_db import Marketer

# تعريف الـ Blueprint
suppliers_bp = Blueprint('suppliers_auth', __name__, template_folder='templates')

@suppliers_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    بوابة تسجيل دخول الموردين والمسوقين المحسنة.
    """
    if request.method == 'GET':
        if current_user.is_authenticated and session.get('user_type') == 'supplier':
            return redirect(url_for('suppliers_dashboard.dashboard'))
        return render_template('suppliers_auth_portal/login.html')

    try:
        # التعديل: قبول JSON أو Form Data لضمان عدم توقف الطلبات
        data = request.get_json(silent=True) or request.form.to_dict()
        
        if not data:
            return jsonify({"status": "error", "message": "بيانات غير صالحة"}), 400

        login_type = data.get('type')
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not login_type or not username or not password:
            return jsonify({"status": "error", "message": "يجب إدخال اسم المستخدم وكلمة المرور"}), 400

        # --- منطق دخول المسوقين ---
        if login_type == 'marketer':
            user = Marketer.query.filter_by(marketing_code=username).first()
            # استخدام hasattr للتأكد من وجود دالة التحقق قبل استدعائها
            if user and hasattr(user, 'check_password') and user.check_password(password):
                login_user(user, remember=True)
                session['user_type'] = 'supplier' 
                session.modified = True
                return jsonify({"status": "success", "redirect": url_for('suppliers_dashboard.dashboard')})
            return jsonify({"status": "error", "message": "بيانات دخول المسوق غير صحيحة"}), 401

        # --- منطق دخول الموردين ---
        if login_type == 'supplier':
            supplier = Supplier.query.filter(
                (Supplier.search_phone == username) | (Supplier.username == username)
            ).first()
            
            # استخدام hasattr للتأكد من وجود دالة التحقق قبل استدعائها
            if supplier and hasattr(supplier, 'check_password') and supplier.check_password(password):
                login_user(supplier, remember=True)
                session['user_type'] = 'supplier'
                session.modified = True
                return jsonify({"status": "success", "redirect": url_for('suppliers_dashboard.dashboard')})
            return jsonify({"status": "error", "message": "بيانات دخول المورد غير صحيحة"}), 401

        return jsonify({"status": "error", "message": "نوع دخول غير معروف"}), 400

    except Exception as e:
        # إظهار تفاصيل الخطأ في السجلات لمساعدتك في التصحيح
        return jsonify({"status": "error", "message": f"خطأ في السيرفر: {str(e)}"}), 500

@suppliers_bp.route('/logout')
def logout():
    """
    تسجيل خروج آمن مع مسح كامل للجلسة.
    """
    logout_user()
    session.clear() 
    response = make_response(redirect(url_for('suppliers_auth.login')))
    response.set_cookie('session', '', expires=0, path='/')
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

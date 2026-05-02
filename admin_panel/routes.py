from flask import render_template, request, redirect, url_for, flash, session
from core import db 

# استيراد النماذج (Models) بمساراتها الصحيحة
try:
    from core.models import Vendor, User
    from core.models.vendor import WithdrawRequest
except ImportError:
    WithdrawRequest = None
    Vendor = None
    User = None

from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """بوابة الدخول السيادية لمركز القيادة"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن القائد في الترسانة الرقمية
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if user.role == 'admin':
                session['admin_id'] = user.id
                session['admin_name'] = user.username
                flash(f"أهلاً بك ياقائد {user.username}، تم تفعيل مركز المراقبة.", "success")
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash("تنبيه: لا تملك صلاحيات الوصول لهذه المنطقة السيادية.", "danger")
        else:
            flash("خطأ: بيانات الدخول غير صحيحة، حاول مجدداً.", "danger")
            
    return render_template('login.html')

@admin_bp.route('/logout')
def logout():
    """إغلاق جلسة الوصول وتأمين النظام"""
    session.clear()
    flash("تم تسجيل الخروج وتأمين مركز القيادة بنجاح.", "info")
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
def admin_dashboard():
    """مركز المراقبة والإحصائيات الرئيسي"""
    if 'admin_id' not in session:
        return redirect(url_for('admin.login'))
    return render_template('dashboard.html')

@admin_bp.route('/withdraw-requests')
def withdraw_requests():
    """عرض كافة طلبات تصفية الأرصدة المعلقة"""
    if 'admin_id' not in session:
        return redirect(url_for('admin.login'))
        
    if WithdrawRequest is None:
        flash("تنبيه: نظام طلبات السحب غير مفعل حالياً.", "warning")
        return render_template('withdraw_requests.html', requests=[])
    
    try:
        pending_requests = WithdrawRequest.query.filter_by(status='pending').order_by(WithdrawRequest.created_at.desc()).all()
        return render_template('withdraw_requests.html', requests=pending_requests)
    except Exception as e:
        flash(f"حدث خطأ أثناء جلب البيانات: {str(e)}", "danger")
        return render_template('withdraw_requests.html', requests=[])

@admin_bp.route('/finalize-withdrawal', methods=['POST'])
def finalize_withdrawal():
    """تعميد الحوالات وأرشفتها في السجلات"""
    if 'admin_id' not in session:
        return redirect(url_for('admin.login'))

    request_id = request.form.get('request_id')
    bank_name = request.form.get('bank_name')
    reference_number = request.form.get('reference_number')

    withdrawal_entry = WithdrawRequest.query.get(request_id)
    if withdrawal_entry:
        try:
            withdrawal_entry.status = 'completed'
            withdrawal_entry.bank_used = bank_name
            withdrawal_entry.reference_id = reference_number
            db.session.commit()
            flash(f"تم تعميد الحوالة ({reference_number}) بنجاح.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"فشل نظام الأرشفة: {str(e)}", "danger")
    
    return redirect(url_for('admin.withdraw_requests'))

@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
def add_supplier():
    """إضافة مورد جديد للشبكة"""
    if 'admin_id' not in session:
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        try:
            new_vendor = Vendor(name=name, city=city)
            db.session.add(new_vendor)
            db.session.commit()
            flash(f"تم إضافة المورد ({name}) بنجاح.", "success")
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"خطأ في الحفظ: {str(e)}", "danger")

    return render_template('add_supplier.html')

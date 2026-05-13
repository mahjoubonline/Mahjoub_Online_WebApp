# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models.supplier_db import db, Supplier  
from datetime import datetime
from functools import wraps

# تعريف الـ Blueprint باسم يتوافق مع استدعاءات run.py و auth/routes.py
admin_bp = Blueprint('admin_dashboard', __name__, template_folder='templates')

def login_required(f):
    """مغلف التحقق من الهوية السيادية"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """
    عرض لوحة التحكم الرئيسية
    يتم هنا استدعاء dashboard_content.html الذي بدوره يرث من admin_base.html
    """
    return render_template('admin/dashboard_content.html')

@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """واجهة تعميد وإضافة الموردين للمنظومة"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form

        try:
            # إنشاء سجل المورد الجديد بناءً على المعايير المعتمدة
            new_supplier = Supplier(
                username=data.get('username'),
                password=data.get('password', '123456'), # كلمة مرور مؤقتة
                trade_name=data.get('trade_name'),
                owner_name=data.get('owner_name'),
                activity_type=data.get('activity_type'),
                phone=data.get('phone'),
                bank_name=data.get('bank_name'),
                bank_acc=data.get('bank_acc'),
                province=data.get('province'),
                district=data.get('district'),
                sovereign_id=f"SUP-{datetime.now().strftime('%Y%m%d%H%M')}",
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_supplier)
            db.session.commit()
            
            return jsonify({
                "status": "success", 
                "message": f"تم تعميد المورد {data.get('trade_name')} بنجاح."
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"عطل فني: {str(e)}"}), 500

    # في حالة GET، يتم عرض صفحة الإضافة داخل الهيكل العام
    return render_template('admin/add_supplier.html', next_id=963)

@admin_bp.route('/suppliers-list')
@login_required
def list_suppliers():
    """عرض قائمة الموردين المعتمدين في النظام"""
    suppliers = Supplier.query.order_by(Supplier.created_at.desc()).all()
    return render_template('admin/list_suppliers.html', suppliers=suppliers)

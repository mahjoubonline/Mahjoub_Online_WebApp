from flask import Blueprint, render_template, request, jsonify, session
from models.supplier_db import db, Supplier  
from datetime import datetime
from functools import wraps

# تصحيح الاسم ليتوافق مع ملف run.py
admin_bp = Blueprint('admin_dashboard', __name__, template_folder='templates')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({"status": "error", "message": "يجب تسجيل الدخول أولاً"}), 401
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        # استقبال البيانات سواء كانت JSON أو Form
        data = request.get_json() if request.is_json else request.form

        try:
            # استخدام أسماء الحقول الدقيقة الموجودة في models/supplier_db.py
            new_supplier = Supplier(
                username=data.get('username'),
                password=data.get('password', '123456'), # كلمة سر افتراضية
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
                "message": f"تم تعميد المورد {data.get('trade_name')} بنجاح في النظام السيادي."
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"خطأ تقني: {str(e)}"}), 500

    # عرض الواجهة (GET)
    return render_template('admin/add_supplier.html', next_id=963)

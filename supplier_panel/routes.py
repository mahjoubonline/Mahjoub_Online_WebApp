from flask import Blueprint, render_template

supplier_bp = Blueprint('supplier', __name__, 
                        template_folder='templates',
                        static_folder='static')

@supplier_bp.route('/supplier/login')
def login():
    # تأكد من وجود المجلد supplier داخل templates الموردين
    return "<h1>بوابة الموردين قيد التجهيز</h1>"

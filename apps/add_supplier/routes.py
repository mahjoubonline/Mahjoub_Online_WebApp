# coding: utf-8
# 🔑 محرك الموردين الحوكمي والسيادي - منصة محجوب أونلاين 2026

from flask import render_template, request, jsonify, current_app, url_for
from flask_login import login_required, current_user
import jinja2

# استيراد البلوبرينت المعزول الخاص بالموردين
from . import admin_suppliers
# 💡 استيراد موديل قاعدة البيانات الفعلي لديك ليعمل الفحص بشكل صحيح
from apps.models import Supplier  

def generate_sovereign_id():
    """
    سحب آخر رقم مورد من قاعدة البيانات وزيادة العداد بمقدار 1 تلقائياً ليكون المعرف القادم دقيقاً.
    النمط المعتمد والثابت بالداتابيز: SUP-WEL-MAH963
    """
    prefix = "SUP-WEL-MAH963"
    default_id = f"{prefix}19"
    
    try:
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        
        if last_supplier and last_supplier.sovereign_id:
            last_code = last_supplier.sovereign_id.strip()
            if last_code.startswith(prefix):
                num_part_str = last_code.replace(prefix, "")
                if num_part_str.isdigit():
                    next_num = int(num_part_str) + 1
                    return f"{prefix}{next_num}"
    except Exception as e:
        current_app.logger.error(f"❌ خطأ أثناء احتساب الرقم الحوكمي التالي: {str(e)}")
    
    return default_id


# ضبط الـ endpoint ليدعم الاسمين معاً لمنع خطأ الـ BuildError تماماً أثناء المزامنة
@admin_suppliers.route('/add', methods=['GET', 'POST'], endpoint='add_supplier_page')
@admin_suppliers.route('/add_legacy', methods=['GET', 'POST'], endpoint='add_supplier')
@login_required
def add_supplier_page():
    if request.method == 'POST':
        # استقبال البيانات من الفورم عند الحفظ
        username = request.form.get('username')
        sovereign_id = request.form.get('sovereign_id')
        
        # [منطق الحفظ في قاعدة البيانات هنا]
        
        return jsonify({
            "status": "success",
            "message": "تم تعميد المورد بنجاح في النظام الحوكمي الموحد.",
            "data": {"username": username, "sovereign_id": sovereign_id}
        }), 200

    sovereign_id = generate_sovereign_id()
    
    # تأمين إرسال متغيرات فارغة لـ CSRF لتجنب الانهيار إذا لم تكن الإضافة مثبتة في بيئة معينة
    csrf_val = ""
    try:
        if 'csrf' in current_app.extensions:
            from flask_wtf.csrf import generate_csrf
            csrf_val = generate_csrf()
    except Exception:
        pass

    try:
        return render_template('admin/add_supplier.html', sovereign_id=sovereign_id, owner=current_user, backup_csrf=csrf_val)
    except jinja2.exceptions.TemplateNotFound:
        return render_template('add_supplier.html', sovereign_id=sovereign_id, owner=current_user, backup_csrf=csrf_val)


@admin_suppliers.route('/check-duplicate', methods=['GET'])
@login_required
def check_duplicate():
    """
    الفحص الفوري واللحظي عبر قاعدة البيانات للحقول السبعة لمنع التكرار البنيوي في المنصة.
    إذا كانت القيمة موجودة مسبقاً ترجع (exists: true) لتظهر إشارة الخطر (X) في الواجهة.
    """
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()
    
    if not check_type or not value:
        return jsonify({"exists": False, "error": "Missing parameters"}), 400
        
    exists = False
    try:
        # ربط شروط الفحص للحقول السبعة مباشرة بالموديل (Supplier) والتحقق من التكرار
        if check_type == 'username':
            exists = Supplier.query.filter_by(username=value).first() is not None
            
        elif check_type == 'identity_number':
            exists = Supplier.query.filter_by(identity_number=value).first() is not None
            
        elif check_type == 'owner_name':
            exists = Supplier.query.filter_by(owner_name=value).first() is not None
            
        elif check_type == 'trade_name':
            exists = Supplier.query.filter_by(trade_name=value).first() is not None
            
        elif check_type == 'owner_phone':
            exists = Supplier.query.filter_by(owner_phone=value).first() is not None
            
        elif check_type == 'shop_phone':
            exists = Supplier.query.filter_by(shop_phone=value).first() is not None
            
        elif check_type == 'bank_acc':
            exists = Supplier.query.filter_by(bank_acc=value).first() is not None

    except Exception as e:
        current_app.logger.error(f"❌ خطأ في فحص التكرار اللحظي داخل قاعدة البيانات للحقل {check_type}: {str(e)}")
        return jsonify({"exists": False, "error": "Database query error"}), 500
        
    return jsonify({"exists": exists})

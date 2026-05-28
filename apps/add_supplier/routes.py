# coding: utf-8
# 🛡️ معالج الموردين - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request, jsonify

# تعريف البلوبرينت
# template_folder='templates' تعني أن Flask سيبحث داخل مجلد templates الموجود في نفس المجلد
add_supplier = Blueprint('add_supplier', __name__, template_folder='templates')

@add_supplier.route('/add_supplier', methods=['GET'])
def add_supplier_page():
    """عرض نموذج تعميد المورد"""
    # المسار يبدأ من داخل مجلد templates المذكور أعلاه
    return render_template('admin/add_supplier.html')

@add_supplier.route('/add_supplier_submit', methods=['POST'])
def add_supplier_submit():
    """استلام ومعالجة البيانات المشفرة القادمة من النموذج"""
    try:
        # استلام البيانات المشفرة من الحقل المخفي في النموذج
        encrypted_data = request.form.get('full_encrypted_data')
        
        if not encrypted_data:
            print("⚠️ تحذير: محاولة إرسال فارغة من نموذج تعميد المورد")
            return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400

        # Debug log للتحقق من وصول البيانات في السجلات
        print(f"✅ تم استلام بيانات مشفرة بنجاح، الطول: {len(encrypted_data)}")

        # ملاحظة: يمكنك هنا إضافة كود فك التشفير أو الحفظ في قاعدة البيانات
        
        return jsonify({
            "status": "success", 
            "message": "تم استلام ومعالجة بيانات المورد بنجاح."
        })

    except Exception as e:
        print(f"❌ خطأ فادح في معالجة طلب المورد: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ أثناء المعالجة"}), 500

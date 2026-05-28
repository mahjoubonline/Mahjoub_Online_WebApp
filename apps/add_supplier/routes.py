# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
import json
import base64

# تعريف البلوبرينت (تأكد أن الاسم يطابق ما هو مستخدم في __init__.py)
add_supplier = Blueprint('add_supplier', __name__, template_folder='templates')

@add_supplier.route('/add_supplier', methods=['GET'])
def render_form():
    """عرض نموذج تعميد المورد"""
    return render_template('admin/full_encrypted_supplier_form.html')

@add_supplier.route('/add_supplier_submit', methods=['POST'])
def add_supplier_submit():
    """استلام ومعالجة البيانات المشفرة"""
    try:
        # استلام البيانات المشفرة من النموذج
        encrypted_payload = request.form.get('full_encrypted_data')
        
        if not encrypted_payload:
            return jsonify({"status": "error", "message": "لم يتم استلام بيانات مشفرة"}), 400

        # في حالتنا الحالية (بعد تحييد Crypto)، سنقوم باستلام البيانات
        # إذا كنت ستطبق التشفير لاحقاً، ستفك هنا باستخدام AES
        # مؤقتاً: سنقوم بطباعة البيانات للتأكد من وصولها
        print(f"DEBUG: Data Received: {encrypted_payload}")

        # منطق الحفظ في قاعدة البيانات
        # new_supplier = Supplier(...) 
        # db.session.add(new_supplier)
        # db.session.commit()

        return jsonify({
            "status": "success", 
            "message": "تم استلام طلب تعميد المورد بنجاح، سيتم معالجة البيانات السيادية."
        })

    except Exception as e:
        print(f"❌ خطأ في معالجة طلب المورد: {e}")
        return jsonify({"status": "error", "message": "حدث خطأ داخلي في المعالجة"}), 500

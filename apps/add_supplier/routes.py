from flask import Blueprint, render_template, request, jsonify, url_for, redirect
import os

# تعريف البلوبرينت باسم فريد
admin_suppliers = Blueprint('admin_suppliers', __name__, template_folder='templates')

@admin_suppliers.route('/add', methods=['GET', 'POST'])
def add_supplier():
    # في حالة طلب الصفحة (فتح النموذج)
    if request.method == 'GET':
        # هنا يمكنك جلب آخر ID من قاعدة البيانات لإظهاره في "المعرف السيادي"
        # مثال افتراضي:
        next_id = 96310  
        return render_template('admin/add_supplier.html', next_id=next_id)

    # في حالة إرسال البيانات (الضغط على زر إتمام التعميد)
    if request.method == 'POST':
        try:
            # استقبال البيانات النصية من الفورم
            username = request.form.get('username')
            trade_name = request.form.get('trade_name')
            phone = request.form.get('phone')
            
            # استقبال ملف الصورة (صورة الهوية)
            identity_image = request.files.get('identity_image')
            
            if identity_image:
                # منطق حفظ الصورة في مجلد uploads
                filename = f"id_{username}.jpg"
                # identity_image.save(os.path.join('uploads/ids', filename))
                pass

            # --- هنا تضع كود الحفظ في قاعدة البيانات ---
            
            # الرد بصيغة JSON ليتناسب مع دالة fetch و SweetAlert2 في الصفحة
            return jsonify({
                "status": "success",
                "message": f"تم تعميد المورد {trade_name} بنجاح في النظام السيادي."
            }), 200

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

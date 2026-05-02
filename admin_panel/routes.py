from flask import render_template, request, redirect, url_for, flash
# الحل الصحيح بناءً على ملف core/__init__.py:
# نستورد db من مجلد core وليس من app
from core import db 
# نستورد النماذج من مسارها الصحيح داخل core
from core.models.user import User # مثال لاستيراد المستخدم
# تأكد من استيراد نموذج طلبات السحب من مساره الصحيح، لنفترض أنه في core.models.finance
# من ملف models الحقيقي لديك:
from models import WithdrawRequest 

# نستورد الـ Blueprint المعرف في __init__.py الخاص بالمجلد الحالي
from . import admin_bp

@admin_bp.route('/withdraw-requests')
def withdraw_requests():
    """
    عرض كافة طلبات تصفية الأرصدة المعلقة للموردين.
    """
    try:
        # جلب الطلبات المعلقة وترتيبها من الأحدث (status = pending)
        pending_requests = WithdrawRequest.query.filter_by(status='pending').order_by(WithdrawRequest.created_at.desc()).all()
        return render_template('withdraw_requests.html', requests=pending_requests)
    except Exception as e:
        flash(f"حدث خطأ أثناء جلب البيانات: {str(e)}", "danger")
        return render_template('withdraw_requests.html', requests=[])

@admin_bp.route('/finalize-withdrawal', methods=['POST'])
def finalize_withdrawal():
    """
    دالة التعميد المالي السيادي لأرشفة بيانات التحويل وتصفية الأرصدة.
    """
    request_id = request.form.get('request_id')
    bank_name = request.form.get('bank_name')
    reference_number = request.form.get('reference_number')

    if not request_id or not reference_number:
        flash("تنبيه: يجب إدخال رقم الحوالة المرجعي لإتمام عملية التعميد ياقائد.", "warning")
        return redirect(url_for('admin.withdraw_requests'))

    # البحث عن طلب السحب في قاعدة البيانات
    withdrawal_entry = WithdrawRequest.query.get(request_id)

    if not withdrawal_entry:
        flash("خطأ: لم يتم العثور على سجل لهذا الطلب في النظام.", "danger")
        return redirect(url_for('admin.withdraw_requests'))

    try:
        # تحديث بيانات السجل المالي للتعميد والأرشفة
        withdrawal_entry.status = 'completed'
        withdrawal_entry.bank_used = bank_name
        withdrawal_entry.reference_id = reference_number
        
        # حفظ التغييرات نهائياً في قاعدة بيانات محجوب أونلاين
        db.session.commit()
        
        flash(f"تم تعميد الحوالة رقم ({reference_number}) بنجاح وأرشفة الطلب في سجلات السيادة المالية.", "success")
        
    except Exception as e:
        db.session.rollback() # التراجع في حالة وجود أي خلل تقني لضمان سلامة الأرصدة
        flash(f"فشل نظام الأرشفة في معالجة الطلب: {str(e)}", "danger")

    return redirect(url_for('admin.withdraw_requests'))

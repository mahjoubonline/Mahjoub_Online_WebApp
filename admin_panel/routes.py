from flask import Blueprint, render_template, request, redirect, url_for, flash
# استيراد قاعدة البيانات والنماذج البرمجية
from app import db 
from models import WithdrawRequest, Vendor 

# تعريف الـ Blueprint الخاص بلوحة الإدارة
admin = Blueprint('admin', __name__)

@admin.route('/withdraw-requests')
def withdraw_requests():
    """
    عرض كافة طلبات تصفية الأرصدة المعلقة للموردين.
    يتم جلب البيانات حية من قاعدة البيانات لضمان الدقة المالية.
    """
    try:
        # جلب الطلبات التي تنتظر التعميد (status = pending)
        # يتم ترتيبها من الأحدث إلى الأقدم
        pending_requests = WithdrawRequest.query.filter_by(status='pending').order_by(WithdrawRequest.created_at.desc()).all()
        
        return render_template('withdraw_requests.html', requests=pending_requests)
    
    except Exception as e:
        flash(f"حدث خطأ أثناء جلب البيانات: {str(e)}", "danger")
        return render_template('withdraw_requests.html', requests=[])

@admin.route('/finalize-withdrawal', methods=['POST'])
def finalize_withdrawal():
    """
    دالة التعميد المالي السيادي:
    1. تستقبل بيانات الحوالة المرجعية وجهة التحويل.
    2. تقوم بتحديث حالة الطلب إلى 'مكتمل'.
    3. تؤرشف بيانات التحويل لضمان عدم تكرار المطالبة المالية.
    """
    request_id = request.form.get('request_id')
    bank_name = request.form.get('bank_name')
    reference_number = request.form.get('reference_number')

    # التحقق من وجود البيانات الأساسية لضمان سلامة الأرشفة
    if not request_id or not reference_number:
        flash("تنبيه: يجب إدخال رقم الحوالة المرجعي لإتمام عملية التعميد.", "warning")
        return redirect(url_for('admin.withdraw_requests'))

    # البحث عن طلب السحب المحدد
    withdrawal_entry = WithdrawRequest.query.get(request_id)

    if not withdrawal_entry:
        flash("خطأ: لم يتم العثور على سجل لهذا الطلب في النظام.", "danger")
        return redirect(url_for('admin.withdraw_requests'))

    try:
        # تحديث بيانات السجل المالي
        withdrawal_entry.status = 'completed'
        withdrawal_entry.bank_used = bank_name
        withdrawal_entry.reference_id = reference_number
        
        # حفظ التغييرات نهائياً في قاعدة البيانات
        db.session.commit()
        
        flash(f"تم تعميد الحوالة رقم ({reference_number}) بنجاح. تم تصفية رصيد المورد وأرشفة الطلب.", "success")
        
    except Exception as e:
        # التراجع عن العملية في حال حدوث أي خلل تقني لضمان سلامة البيانات
        db.session.rollback()
        flash(f"فشل نظام الأرشفة في معالجة الطلب: {str(e)}", "danger")

    return redirect(url_for('admin.withdraw_requests'))

# يمكنك إضافة مسارات أخرى خاصة بلوحة الإدارة هنا مستقبلاً

# coding: utf-8
from flask import render_template, make_response, flash
from flask_login import login_required
from apps.statement.routes import statement_blueprint # تأكد من استيراد الـ Blueprint الصحيح

@statement_blueprint.route('/api/statement/report/pdf', methods=['GET'])
@login_required
def export_report_pdf():
    # استيراد ذكي (Lazy Import) داخل الدالة فقط
    try:
        from weasyprint import HTML
    except ImportError:
        return "❌ خطأ: مكتبة توليد ملفات PDF غير مثبتة على السيرفر (WeasyPrint missing).", 500

    try:
        # 1. جلب البيانات
        from apps.models.statement_db import SupplierStatement
        data = SupplierStatement.query.all() 
        
        # 2. تجهيز الـ HTML
        rendered = render_template('pdf_template.html', report_data=data)
        
        # 3. تحويل HTML إلى PDF
        pdf = HTML(string=rendered).write_pdf()
        
        # 4. إعداد الرد
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=statement.pdf'
        
        return response
        
    except Exception as e:
        return f"❌ خطأ أثناء توليد التقرير: {str(e)}", 500

# coding: utf-8
# 📂 apps/statement/routes.py

from flask import render_template, request, jsonify
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.models.supplier_db import Supplier
from apps.utils.report_generator import ReportGenerator  # استدعاء محرك التقارير المركزي
from sqlalchemy import or_
from datetime import datetime

@statement_blueprint.route('/view', methods=['GET'])
@login_required
def view_statement():
    currencies = ['USD', 'YER', 'SAR'] 
    return render_template('admin/statement.html', currencies=currencies)


# 1. البحث الذكي المتوافق بالكامل مع متطلبات الـ Select2 في الواجهة
@statement_blueprint.route('/api/suppliers/search', methods=['GET'])
@login_required
def api_search_suppliers():
    term = request.args.get('q', '')
    if not term:
        return jsonify({"results": []})

    # استعلام ذكي يبحث في كافة تفاصيل المورد
    suppliers = Supplier.query.filter(or_(
        Supplier.trade_name.ilike(f'%{term}%'),
        Supplier.sovereign_id.ilike(f'%{term}%'),
        Supplier.store_name.ilike(f'%{term}%'),
        Supplier.owner_name.ilike(f'%{term}%')
    )).limit(15).all()
    
    # تنسيق العرض للمستخدم في القائمة المنسدلة لـ Select2
    results = [
        {
            'id': s.id, 
            'text': f"{s.trade_name} | {s.store_name} (المالك: {s.owner_name}) - المعرف: {s.sovereign_id}"
        } for s in suppliers
    ]
    return jsonify({"results": results})


# 2. جلب كشف الحساب الشامل والتقارير المالي عبر استدعاء الـ ReportGenerator
@statement_blueprint.route('/api/statement/report', methods=['GET'])
@login_required
def api_get_report():
    s_id = request.args.get('id')
    curr = request.args.get('currency', 'ALL')
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    if not s_id:
        return jsonify({'error': 'يرجى تحديد المورد أولاً'}), 400

    supplier = Supplier.query.get(s_id)
    if not supplier: 
        return jsonify({'error': 'المورد غير موجود بالشرائح الحالية'}), 404

    # تحويل نصوص التواريخ القادمة من daterangepicker إلى كائنات datetime متوافقة مع قاعدة البيانات
    start_date = None
    end_date = None
    
    try:
        if start_str:
            start_date = datetime.strptime(start_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        if end_str:
            end_date = datetime.strptime(end_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
    except ValueError:
        return jsonify({'error': 'صيغة التاريخ غير صحيحة'}), 400

    # أ. استخراج الحركات التفصيلية للمورد من قاعدة البيانات عبر المحرك المركزي
    statements = ReportGenerator.get_detailed_transactions(
        supplier_id=supplier.id, 
        currency=curr, 
        start_date=start_date, 
        end_date=end_date
    )

    # ب. حساب صافي أرباح المنصة المرتبطة بالمورد والمحفظة عبر المحرك المركزي
    total_profit = ReportGenerator.calculate_net_profit(
        currency=curr, 
        start_date=start_date, 
        end_date=end_date
    )

    # ج. تجميع وإرسال البيانات بصيغة JSON النهائية لتغذية جدول الواجهة الفورية
    return jsonify({
        'summary': {
            'total_debit': float(sum(s.debit for s in statements)),
            'total_credit': float(sum(s.credit for s in statements)),
            'net_balance': float(sum(s.credit for s in statements) - sum(s.debit for s in statements)),
            'total_profit': float(total_profit)
        },
        'details': [{
            'date': s.created_at.strftime('%Y-%m-%d %H:%M'),
            'desc': s.description or '---',
            'ref': s.reference_number or '---',
            'currency': s.currency,
            'debit': float(s.debit),
            'credit': float(s.credit),
            'balance': float(s.running_balance)
        } for s in statements]
    })

# coding: utf-8
# 🔑 محرك الموردين الحوكمي والسيادي - منصة محجوب أونلاين 2026

from flask import render_template, request, jsonify, current_app, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import jinja2
import re  # مكتبة التعبيرات النمطية لمعالجة النصوص واستخراج الأرقام بدقة

# استيراد البلوبرينت المعزول الخاص بالموردين وكائن قاعدة البيانات
from . import admin_suppliers
from apps import db
from apps.models import Supplier  

def get_expected_sovereign_id():
    """
    سحب آخر معرف سيادي مسجل في قاعدة البيانات بدقة من خلال قراءة الجزء الرقمي 
    الأخير وزيادته بمقدار 1، ليعرض للمسؤول في الواجهة المعرف المتوقع تماماً.
    """
    default_prefix = "SUP-WEL-MAH"
    try:
        # جلب آخر مورد تم تسجيله بناءً على أعلى رقم ID في الجدول
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        
        if last_supplier and last_supplier.sovereign_id:
            sovereign_str = last_supplier.sovereign_id.strip()
            
            # استخراج كافة الأرقام المتتالية في نهاية المعرف السيادي
            match = re.search(r'\d+$', sovereign_str)
            if match:
                last_num = int(match.group())
                next_num = last_num + 1
                
                # استخراج البادئة النصية الديناميكية التي تسبق الرقم مباشرة (مثل SUP-WEL-MAH)
                prefix_match = re.match(r'^(.*?)(\d+)$', sovereign_str)
                if prefix_match:
                    return f"{prefix_match.group(1)}{next_num}"
                
                return f"{default_prefix}{next_num}"
        
        # ملاذ آمن: في حال وجود سجلات لا تطابق النمط المعتاد في النظام
        if last_supplier:
            return f"{default_prefix}96319"

    except Exception as e:
        current_app.logger.error(f"❌ خطأ أثناء احتساب المعرف السيادي القادم: {str(e)}")
    
    # في حال كان الجدول فارغاً تماماً في البداية
    return f"{default_prefix}96319"


@admin_suppliers.route('/add', methods=['GET', 'POST'], endpoint='add_supplier_page')
@admin_suppliers.route('/add_legacy', methods=['GET', 'POST'], endpoint='add_supplier')
@login_required
def add_supplier_page():
    if request.method == 'POST':
        try:
            # 1. استقبال البيانات السبعة والبيانات المساعدة من الواجهة
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            identity_type = request.form.get('identity_type', '').strip()
            identity_number = request.form.get('identity_number', '').strip()
            owner_name = request.form.get('owner_name', '').strip()
            trade_name = request.form.get('trade_name', '').strip()
            owner_phone = request.form.get('owner_phone', '').strip()
            shop_phone = request.form.get('shop_phone', '').strip()
            province = request.form.get('province', '').strip()
            district = request.form.get('district', '').strip()
            address_detail = request.form.get('address_detail', '').strip()
            fin_type = request.form.get('fin_type', '').strip()
            bank_name = request.form.get('bank_name', '').strip()
            bank_acc = request.form.get('bank_acc', '').strip()
            activity_type = request.form.get('activity_type', '').strip()

            # 2. فحص الحقول السبعة بشكل صارم في الخلفية قبل إتمام الحفظ لمنع تجاوز التكرار
            check_fields = {
                "username": (Supplier.query.filter_by(username=username).first(), "اسم المستخدم (Login)"),
                "identity_number": (Supplier.query.filter_by(identity_number=identity_number).first(), "رقم الوثيقة / الهوية"),
                "owner_name": (Supplier.query.filter_by(owner_name=owner_name).first(), "اسم المالك الكامل"),
                "trade_name": (Supplier.query.filter_by(trade_name=trade_name).first(), "الاسم التجاري للمنشأة"),
                "owner_phone": (Supplier.query.filter_by(owner_phone=owner_phone).first(), "رقم هاتف المالك"),
                "shop_phone": (Supplier.query.filter_by(shop_phone=shop_phone).first(), "هاتف المنشأة (محل)"),
                "bank_acc": (Supplier.query.filter_by(bank_acc=bank_acc).first(), "رقم الحساب")
            }

            for key, (exists, field

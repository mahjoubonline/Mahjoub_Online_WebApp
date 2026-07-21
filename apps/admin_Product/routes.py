# coding: utf-8
# 📂 apps/admin_Product/routes.py

import uuid
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required
from apps.extensions import db
from apps.models.product_db import Product
from apps.models.product_supplier_map import ProductSupplierMapping
from apps.services.product_sync_service import sync_products_from_qomra

admin_product_bp = Blueprint(
    'admin_product_bp', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

@admin_product_bp.route('/products', methods=['GET'])
@login_required
def manage_products():
    """عرض إدارة المنتجات مع دعم البحث الفوري (Live Search) وترقيم ديناميكي (15 منتجاً في كل صفحة)."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    
    # تثبيت عدد المنتجات في كل صفحة على 15 منتجاً مع حساب الصفحات ديناميكياً حسب النمو اللحظي
    per_page = 15 
    
    # بناء الاستعلام مع دعم البحث بالاسم
    query = Product.query
    if search_query:
        query = query.filter(Product.title.ilike(f'%{search_query}%'))
        
    # تنفيذ الترقيم الديناميكي لحظياً بناءً على إجمالي المنتجات في قاعدة البيانات
    pagination_obj = query.order_by(Product.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    products = pagination_obj.items
    
    # هيكل بيانات الترقيم المتوافق مع القوالب
    pagination = {
        'currentPage': pagination_obj.page,
        'totalPages': pagination_obj.pages,
        'totalItems': pagination_obj.total
    }
    
    # إذا كان الطلب قادماً عبر AJAX للبحث الفوري، يتم إرجاع القالب لتحديث حاوية النتائج
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template(
            'admin/admin_Product.html', 
            products=products, 
            pagination=pagination, 
            search=search_query
        )
        
    return render_template(
        'admin/admin_Product.html', 
        products=products, 
        pagination=pagination, 
        search=search_query
    )

@admin_product_bp.route('/save-sync', methods=['POST'])
@login_required
def save_sync():
    """تنفيذ عملية مزامنة المنتجات ديناميكياً مع قمرة وإرجاع النتيجة بصيغة JSON متوافقة مع المودال."""
    try:
        # استدعاء خدمة المزامنة المحدثة ديناميكياً
        result_message = sync_products_from_qomra()
        return jsonify({
            'status': 'success',
            'message': result_message if isinstance(result_message, str) else 'تمت مزامنة المنتجات بنجاح من قمرة.'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"فشل عملية المزامنة: {str(e)}"
        }), 500

@admin_product_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """إضافة منتج جديد يدوياً وإنشاء رابط سيادي للمورد."""
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            price = float(request.form.get('price', 0))
            quantity = int(request.form.get('quantity', 0))
            description = request.form.get('description', '')
            image_url = request.form.get('image_url', '')

            # توليد qid فريد يدوياً للمنتج المحلي
            product_qid = f"custom_{uuid.uuid4().hex[:10]}"

            new_product = Product(
                qid=product_qid,
                title=title,
                price=price,
                currency='SAR',
                quantity=quantity,
                image_url=image_url,
                description=description
            )
            db.session.add(new_product)

            # إضافة سجل ربط افتراضي في جدول ProductSupplierMapping
            mapping = ProductSupplierMapping(
                product_qid=product_qid,
                supplier_id=1,
                status='active'
            )
            db.session.add(mapping)

            db.session.commit()
            flash('تمت إضافة المنتج بنجاح.', 'success')
            return redirect(url_for('admin_product_bp.manage_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء الإضافة: {str(e)}', 'danger')
            
    return render_template('admin/product_form.html', action='add')

@admin_product_bp.route('/products/edit/<string:qid>', methods=['GET', 'POST'])
@login_required
def edit_product(qid):
    """تعديل منتج محدد بناءً على المعرف الفريد qid."""
    product = Product.query.filter_by(qid=qid).first_or_404()
    
    if request.method == 'POST':
        try:
            product.title = request.form.get('title', product.title)
            product.price = float(request.form.get('price', product.price or 0))
            product.quantity = int(request.form.get('quantity', product.quantity or 0))
            product.description = request.form.get('description', product.description)
            product.image_url = request.form.get('image_url', product.image_url)

            db.session.commit()
            flash('تم تحديث بيانات المنتج بنجاح.', 'success')
            return redirect(url_for('admin_product_bp.manage_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء التحديث: {str(e)}', 'danger')
            
    return render_template('admin/product_form.html', product=product, action='edit')

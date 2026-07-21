# 📂 apps/admin_Product/routes.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required
from apps.models import db, Product
from apps.admin_Product.services import sync_products_from_qomra

admin_product_bp = Blueprint(
    'admin_product_bp', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

@admin_product_bp.route('/products', methods=['GET'])
@login_required
def manage_products():
    """عرض إدارة المنتجات مع دعم البحث الفوري (Live Search) والترقيم (Pagination)."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    per_page = 15  # عدد المنتجات في كل صفحة
    
    # بناء الاستعلام مع دعم البحث بالاسم
    query = Product.query
    if search_query:
        query = query.filter(Product.title.ilike(f'%{search_query}%'))
        
    # تنفيذ الترقيم
    pagination_obj = query.order_by(Product.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    products = pagination_obj.items
    
    # هيكل بيانات الترقيم المتوافق مع القوالب
    pagination = {
        'currentPage': pagination_obj.page,
        'totalPages': pagination_obj.pages,
        'totalItems': pagination_obj.total
    }
    
    # إذا كان الطلب قادماً عبر AJAX للبحث الفوري، يتم إرجاع القالب مباشرة لتحديث حاوية النتائج
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
    """تنفيذ عملية مزامنة المنتجات مع قمرة وإرجاع النتيجة بصيغة JSON متوافقة مع المودال."""
    try:
        # استدعاء خدمة المزامنة
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
    """إضافة منتج جديد يدوياً."""
    if request.method == 'POST':
        try:
            # معالجة بيانات الإضافة هنا
            flash('تمت إضافة المنتج بنجاح.', 'success')
            return redirect(url_for('admin_product_bp.manage_products'))
        except Exception as e:
            flash(f'حدث خطأ أثناء الإضافة: {str(e)}', 'danger')
            
    return render_template('admin/product_form.html', action='add')

@admin_product_bp.route('/products/edit/<string:qid>', methods=['GET', 'POST'])
@login_required
def edit_product(qid):
    """تعديل منتج محدد بناءً على المعرف الفريد qid."""
    product = Product.query.filter_by(qid=qid).first_or_404()
    
    if request.method == 'POST':
        try:
            # معالجة بيانات التحديث هنا
            flash('تم تحديث بيانات المنتج بنجاح.', 'success')
            return redirect(url_for('admin_product_bp.manage_products'))
        except Exception as e:
            flash(f'حدث خطأ أثناء التحديث: {str(e)}', 'danger')
            
    return render_template('admin/product_form.html', product=product, action='edit')

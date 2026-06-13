# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from apps import db
from apps.models.bridge_db import Product, ProductVariant
from apps.utils.bridge_engine import QumraBridgeEngine
import traceback

bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """عرض لوحة التحكم مع نظام الترقيم (Pagination) وتمرير العناوين للبحث الشامل."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 16
        
        # 1. جلب المنتجات المحددة للصفحة الحالية
        pagination = Product.query.order_by(Product.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        products = pagination.items
        
        # 2. جلب قائمة بجميع العناوين للبحث
        all_titles = [p.title for p in Product.query.with_entities(Product.title).all()]
        
        return render_template('admin/bridge_dashboard.html', 
                               products=products, 
                               pagination=pagination, 
                               page=page,
                               all_titles=all_titles)
                               
    except Exception as e:
        print(f"Error in bridge dashboard: {str(e)}")
        flash(f"حدث خطأ: {str(e)}", "danger")
        return redirect(url_for('admin_dashboard.dashboard'))

@bridge_bp.route('/add-product', methods=['GET', 'POST'])
def add_product_page():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            # ... (بقية كود إضافة المنتج كما هو)
            new_product = Product(
                title=title,
                description=request.form.get('description', ''),
                quantity=int(request.form.get('quantity', 0)),
                supplier_id=request.form.get('supplier_id'),
                image_url=request.form.get('image_url') # إضافة رابط الصورة
            )
            new_product.price = str(request.form.get('price', '0'))
            db.session.add(new_product)
            db.session.commit()
            flash('تم إضافة المنتج بنجاح', 'success')
            return redirect(url_for('mahjoub_bridge.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'خطأ أثناء الحفظ: {str(e)}', 'danger')
    return render_template('admin/add_product.html')

@bridge_bp.route('/sync-now', methods=['POST'])
def sync_now():
    """المزامنة مع جلب بيانات الصورة."""
    try:
        engine = QumraBridgeEngine()
        raw_products = engine.fetch_latest_products(limit=100)
        
        if not raw_products or not isinstance(raw_products, list):
            return jsonify({"status": "error", "message": "فشل الاتصال بمحرك المزامنة"})

        count = 0
        for item in raw_products:
            if not isinstance(item, dict): continue
            
            title = str(item.get('title') or "").strip()
            if not title or Product.query.filter_by(title=title).first():
                continue
            
            # استخراج البيانات
            pricing = item.get('pricing')
            raw_price = str(pricing.get('price') if isinstance(pricing, dict) else "0")
            raw_qty = item.get('quantity')
            safe_qty = int(raw_qty) if str(raw_qty or "").isdigit() else 0
            
            # استخراج رابط الصورة (تأكد من المفتاح الصحيح، قد يكون 'image' أو 'image_url')
            image_url = item.get('image_url') or item.get('image') or ""
            
            new_product = Product(
                title=title,
                description="تمت المزامنة تلقائياً",
                quantity=safe_qty,
                supplier_id="QUMRA_SYNC",
                image_url=image_url # حفظ رابط الصورة هنا
            )
            new_product.price = raw_price
            db.session.add(new_product)
            count += 1
        
        db.session.commit()
        return jsonify({"status": "success", "message": f"تمت المزامنة وجلب {count} منتج"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "حدث خطأ تقني"}), 500

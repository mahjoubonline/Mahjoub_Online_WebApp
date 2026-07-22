# coding: utf-8
# 📂 apps/admin_Product/routes_edit.py

import json
import os
from flask import Blueprint, render_template, request, jsonify, url_for, redirect, flash
from apps.services.product_sync_service import ProductSyncService

admin_product_bp = Blueprint('admin_product_bp', __name__, template_folder='templates')

GRAPHQL_TOKEN = os.environ.get('QUMRA_API_KEY', 'YOUR_ADMIN_API_TOKEN') 

@admin_product_bp.route('/products/edit', methods=['GET'])
def edit_product():
    """عرض صفحة تعديل المنتج وتصحيح معرّف الـ QID المزدوج تلقائياً"""
    raw_qid = request.args.get('qid')
    
    if raw_qid:
        if raw_qid.startswith('qid=qid='):
            qid = raw_qid.replace('qid=qid=', 'qid://')
        elif raw_qid.startswith('qid='):
            qid = raw_qid.replace('qid=', '')
        else:
            qid = raw_qid
    else:
        qid = None
    
    if not qid:
        flash("معرف المنتج (qid) مفقود.", "danger")
        return redirect(url_for('admin_product_bp.manage_products'))
    
    sync_service = ProductSyncService(token=GRAPHQL_TOKEN)
    product = sync_service.fetch_product_by_qid(qid)

    if not product:
        return f"""
        <div style="direction: rtl; font-family: Tahoma; padding: 30px; text-align: center;">
            <h2 style="color: #d9534f;">فشل جلب بيانات المنتج!</h2>
            <p>الـ QID المعالج هو: <b>{qid}</b></p>
            <p style="color: #666;">الرجاء مراجعة سجلات الـ Logs في سيرفر Render لمعرفة استجابة الـ GraphQL.</p>
            <br>
            <a href="{url_for('admin_product_bp.manage_products')}" style="background: #2d0b36; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px;">الرجوع لقائمة المنتجات</a>
        </div>
        """, 400

    suppliers = sync_service.fetch_suppliers() if hasattr(sync_service, 'fetch_suppliers') else []
    all_collections = sync_service.fetch_collections() if hasattr(sync_service, 'fetch_collections') else []

    return render_template(
        'admin/admin_edit_product.html',
        product=product,
        all_collections=all_collections,
        suppliers=suppliers
    )


@admin_product_bp.route('/products/save-sync', methods=['POST'])
def save_sync_product():
    """معالجة وحفظ البيانات وتحديث الصور والمتغيرات عبر الـ API"""
    try:
        qid = request.form.get('qid')
        if not qid:
            return jsonify({"status": "error", "message": "معرف المنتج (qid) مفقود."}), 400

        title = request.form.get('title', '')
        slug = request.form.get('slug', '')
        description = request.form.get('description', '')
        status = request.form.get('status', 'DRAFT')
        sku = request.form.get('sku', '')
        supplier_id = request.form.get('supplier_id')
        
        try:
            price = float(request.form.get('price', 0))
            compare_at_price = float(request.form.get('compare_at_price', 0))
            cost_price = float(request.form.get('original_price', 0))
        except ValueError:
            price, compare_at_price, cost_price = 0.0, 0.0, 0.0

        try:
            quantity = int(request.form.get('quantity', 0))
            weight_val = float(request.form.get('weight', 0))
        except ValueError:
            quantity, weight_val = 0, 0.0

        info = {"title": title, "slug": slug, "status": status}
        pricing = {"price": price, "compareAtPrice": compare_at_price, "costPrice": cost_price, "currency": "YER"}
        dims = {"length": 0, "width": 0, "height": 0, "unit": "cm"}
        weight = {"value": weight_val, "unit": "kg"}
        ident = {"sku": sku}

        collection_ids = json.loads(request.form.get('collection_ids', '[]') or '[]')
        
        # معالجة قراءة المتغيرات سواء تم إرسالها كـ JSON string أو كحقول مصفوفات منفصلة (variant_name[])
        variants_raw = request.form.get('variants', '')
        if variants_raw:
            try:
                variants = json.loads(variants_raw)
            except Exception:
                variants = []
        else:
            # تجميع المتغيرات من الحقول التقليدية في حال أُرسلت عبر الـ Form Data المباشرة
            var_names = request.form.getlist('variant_name[]')
            var_prices = request.form.getlist('variant_price[]')
            var_qtys = request.form.getlist('variant_qty[]')
            var_skus = request.form.getlist('variant_sku[]')
            
            variants = []
            for i in range(len(var_names)):
                if var_names[i].strip():
                    try:
                        v_price = float(var_prices[i]) if i < len(var_prices) and var_prices[i] else 0.0
                    except ValueError:
                        v_price = 0.0
                    try:
                        v_qty = int(var_qtys[i]) if i < len(var_qtys) and var_qtys[i] else 0
                    except ValueError:
                        v_qty = 0
                    v_sku = var_skus[i] if i < len(var_skus) else ''
                    
                    variants.append({
                        "name": var_names[i],
                        "price": v_price,
                        "quantity": v_qty,
                        "sku": v_sku
                    })

        removed_images = json.loads(request.form.get('removed_images', '[]') or '[]')
        new_images = request.files.getlist('images')

        sync_service = ProductSyncService(token=GRAPHQL_TOKEN)
        
        success = sync_service.update_product_data(
            qid=qid,
            info=info,
            pricing=pricing,
            dims=dims,
            weight=weight,
            ident=ident,
            desc=description,
            supplier_id=supplier_id,
            collection_ids=collection_ids,
            variants=variants,
            removed_images=removed_images,
            new_images=new_images,
            quantity=quantity
        )

        if not success:
            return jsonify({"status": "error", "message": "فشل حفظ وتحديث التعديلات على الخادم المركزي."}), 500

        return jsonify({"status": "success", "message": "تم حفظ وتحديث المنتج ومزامنة بياناته بنجاح!"})

    except Exception as e:
        print(f"Error saving product sync: {e}")
        return jsonify({"status": "error", "message": f"حدث خطأ أثناء معالجة الطلب: {str(e)}"}), 500


@admin_product_bp.route('/products/manage', methods=['GET'])
def manage_products():
    """عرض قائمة إدارة المنتجات"""
    sync_service = ProductSyncService(token=GRAPHQL_TOKEN)
    page = request.args.get('page', 1, type=int)
    title_query = request.args.get('title', '', type=str)
    
    result = sync_service.fetch_products(page=page, limit=20, title=title_query)
    
    return render_template(
        'admin/admin_manage_products.html',
        products=result.get("data", []),
        pagination=result.get("pagination", None),
        search_title=title_query
    )

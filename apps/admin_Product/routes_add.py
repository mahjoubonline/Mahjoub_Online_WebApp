from flask import render_template, request, redirect, url_for, flash
from .routes import admin_product_bp


@admin_product_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    """
    مسار إضافة منتج جديد إلى منصة السوق.
    - GET: عرض صفحة النموذج الخاص بإضافة المنتج.
    - POST: استلام البيانات، التحقق من صحتها، ثم حفظها وإعادة التوجيه.
    """
    if request.method == 'POST':
        try:
            # 1. استخراج البيانات من نموذج الإدخال (Form Data)
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            price = request.form.get('price', type=float, default=0.0)
            quantity = request.form.get('quantity', type=int, default=0)
            category_id = request.form.get('category_id', '').strip()
            image_url = request.form.get('image_url', '').strip()

            # 2. التحقق من البيانات الأساسية (Validation)
            if not title:
                flash('عفواً، يجب إدخال عنوان المنتج.', 'danger')
                return render_template('admin/add_product.html')

            if price <= 0:
                flash('يرجى تحديد سعر صحيح للمنتج.', 'warning')
                return render_template('admin/add_product.html')

            # 3. بناء هيكل البيانات المخصصة للمنتج
            new_product_payload = {
                "title": title,
                "description": description,
                "pricing": {
                    "price": price
                },
                "quantity": quantity,
                "category_id": category_id,
                "images": [{"fileUrl": image_url}] if image_url else []
            }

            # -------------------------------------------------------------
            # 4. تنفيذ حفظ البيانات (سواء عبر GraphQL Mutation أو Database Query)
            # مثال:
            # response = create_product_mutation(new_product_payload)
            # -------------------------------------------------------------

            flash('تمت إضافة المنتج بنجاح!', 'success')
            return redirect(url_for('admin_product_bp.manage_products'))

        except Exception as e:
            flash(f'حدث خطأ غير متوقع أثناء إضافة المنتج: {str(e)}', 'danger')
            return render_template('admin/add_product.html')

    # في حالة طلب الصفحة بأسلوب GET
    return render_template('admin/add_product.html')

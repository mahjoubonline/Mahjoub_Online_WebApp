from flask import jsonify, flash, redirect, url_for
from apps.services.graphql_client import QomrahGraphQLClient
from apps.services.product_sync_service import ProductSyncService # افترض أن لديك سيرفس المزامنة

@admin_product_bp.route('/sync-products', methods=['POST'])
def sync_products():
    try:
        # استدعاء الجلسة لجلب المنتجات من المنصة
        client = ProductSyncService(token=os.environ.get('QUMRA_API_KEY'))
        
        # جلب الصفحة الأولى كمثال (أو حلقة تكرارية لجلب كل الصفحات)
        raw_data = client.fetch_products(page=1, limit=50)
        
        if not raw_data or "data" not in raw_data:
            flash("فشل في جلب البيانات من الخادم الخارجي.", "danger")
            return redirect(url_for('admin_product_bp.manage_products'))

        # هنا يمكنك حفظ المنتجات في قاعدة البيانات المحلية الخاصة بك
        # client.sync_to_local_db(raw_data)

        flash(f"تمت مزامنة المنتجات بنجاح! تم العثور على {len(raw_data.get('data', []))} منتج.", "success")
    except Exception as e:
        flash(f"حدث خطأ أثناء المزامنة: {str(e)}", "danger")

    return redirect(url_for('admin_product_bp.manage_products'))

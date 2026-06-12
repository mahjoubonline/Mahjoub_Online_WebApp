from apps.utils.bridge_engine import QumraBridgeEngine

@bridge_bp.route('/sync-now', methods=['POST'])
def sync_now():
    """المزامنة اللحظية: جلب البيانات وتخزينها مشفرة"""
    try:
        engine = QumraBridgeEngine()
        # 1. جلب البيانات من المحرك (API)
        raw_products = engine.fetch_latest_products(limit=20)
        
        if not raw_products:
            return jsonify({"status": "warning", "message": "لم يتم العثور على منتجات جديدة أو فشل الاتصال بالـ API"})

        count = 0
        for item in raw_products:
            # 2. التأكد من عدم التكرار
            existing = Product.query.filter_by(title=item.get('title')).first()
            if not existing:
                # 3. إنشاء المنتج (الـ Model في bridge_db يجب أن يتولى التشفير تلقائياً)
                new_product = Product(
                    title=item.get('title'),
                    description="تمت المزامنة تلقائياً",
                    price=item.get('pricing', {}).get('price', 0), # استخراج السعر من الكائن
                    quantity=item.get('quantity', 0),
                    supplier_id="QUMRA_SYNC"
                )
                db.session.add(new_product)
                count += 1
        
        db.session.commit()
        return jsonify({"status": "success", "message": f"تمت المزامنة بنجاح وجلب {count} منتج جديد"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"فشل المزامنة: {str(e)}"}), 500

# 📂 apps/suppliers_auth_portal/routes.py

# ... داخل دالة login ...
        if login_type == 'supplier':
            # نستخدم search_phone للبحث لأننا لا يمكننا البحث في الحقل المشفر مباشرة
            # تأكد أن المدخل (username) تم التعامل معه ليطابق تنسيق الرقم المخزن
            supplier = Supplier.query.filter(
                (Supplier.search_phone == username) | (Supplier.username == username)
            ).first()
            
            if supplier and supplier.check_password(password):
                login_user(supplier, remember=True)
                return jsonify({"status": "success", "redirect": url_for('suppliers.dashboard')})
            return jsonify({"status": "error", "message": "بيانات دخول المورد غير صحيحة"}), 401
# ...

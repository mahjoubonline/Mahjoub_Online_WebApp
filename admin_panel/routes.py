from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from core.models import db, Supplier, Product
from core.qumra_sync import qumra_manager  # استدعاء محرك قمرة الذي صممناه
import os

# تعريف البلوبرنت
admin_bp = Blueprint('admin', __name__)

# --- 1. لوحة التحكم الرئيسية ---
@admin_bp.route('/')
def dashboard():
    try:
        suppliers_count = Supplier.query.count()
        products_count = Product.query.count()
        
        # واجهة بسيطة تعبر عن هوية محجوب أونلاين
        return f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding: 40px; background-color: #f4f4f9;">
            <h1 style="color: #6a0dad; border-bottom: 2px solid #6a0dad; display: inline-block; padding-bottom: 10px;">
                لوحة تحكم محجوب أونلاين 🚀
            </h1>
            <div style="display: flex; justify-content: center; gap: 30px; margin-top: 30px;">
                <div style="background: white; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); padding: 30px; width: 200px;">
                    <h3 style="color: #555;">الموردين</h3>
                    <p style="font-size: 32px; font-weight: bold; color: #6a0dad;">{suppliers_count}</p>
                </div>
                <div style="background: white; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); padding: 30px; width: 200px;">
                    <h3 style="color: #555;">المنتجات</h3>
                    <p style="font-size: 32px; font-weight: bold; color: #6a0dad;">{products_count}</p>
                </div>
            </div>
            <div style="margin-top: 40px;">
                <a href="/admin/sync_now" style="background-color: #6a0dad; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; box-shadow: 0 4px 12px rgba(106, 13, 173, 0.3);">
                    🔄 مزامنة المنتجات من قمرة الآن
                </a>
            </div>
            <p style="margin-top: 25px; color: #2ecc71; font-weight: bold;">✅ حالة الاتصال برندر: متصل</p>
        </div>
        """
    except Exception as e:
        return f"<div style='color:red; text-align:center;'><h2>خطأ في النظام:</h2><p>{str(e)}</p></div>"

# --- 2. تنفيذ مزامنة قمرة ---
@admin_bp.route('/sync_now')
def sync_now():
    # تشغيل محرك المزامنة الذي يستخدم QUMRA_API_KEY و QUMRA_API_URL
    success, message = qumra_manager.fetch_and_sync()
    
    color = "#2ecc71" if success else "#e74c3c"
    icon = "✅" if success else "❌"
    
    return f"""
    <div style="font-family: sans-serif; text-align: center; padding: 50px;">
        <h2 style="color: {color};">{icon} {message}</h2>
        <br>
        <a href="/admin/" style="color: #6a0dad; font-weight: bold; text-decoration: none;">⬅️ العودة للوحة التحكم</a>
    </div>
    """

# --- 3. عرض قائمة الموردين ---
@admin_bp.route('/suppliers')
def list_suppliers():
    suppliers = Supplier.query.all()
    output = "<h2>قائمة الموردين المسجلين</h2><table border='1' style='width:80%; margin:auto; text-align:right; border-collapse:collapse;'>"
    output += "<tr style='background:#6a0dad; color:white;'><th>الاسم</th><th>الهاتف</th><th>الحالة</th></tr>"
    for s in suppliers:
        output += f"<tr><td>{s.name}</td><td>{s.phone}</td><td>{s.status}</td></tr>"
    output += "</table><br><center><a href='/admin/'>العودة</a></center>"
    return output

# --- 4. إضافة مورد تجريبي (للتأكد من القاعدة) ---
@admin_bp.route('/test_add')
def test_add():
    try:
        new_s = Supplier(name="مورد رويال التجريبي", phone="777000000", status="active")
        db.session.add(new_s)
        db.session.commit()
        return "✅ تمت إضافة مورد تجريبي لقاعدة بيانات رندر بنجاح!"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

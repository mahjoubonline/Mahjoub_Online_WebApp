# coding: utf-8
# 📂 apps/suppliers_dashboard/routes/dashboard_routes.py

from flask import Blueprint, render_template, session, redirect, jsonify, request
from flask_login import login_required, current_user
import traceback
import requests
import os

from apps.models import db, Supplier, Order, SupplierWallet
from config import Config

# ✅ تعريف الـ Blueprint بالاسم الصحيح
suppliers_dashboard_bp = Blueprint(
    'suppliers_dashboard',
    __name__,
    template_folder='templates'
)


@suppliers_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    try:
        # ✅ جلب نوع المستخدم
        user_type = session.get('user_type')
        
        # ✅ إذا كانت user_type فارغة، حاول تعيينها تلقائياً
        if not user_type:
            if hasattr(current_user, 'supplier_id') and current_user.supplier_id:
                user_type = 'staff'
                session['user_type'] = 'staff'
            elif hasattr(current_user, 'id'):
                # التحقق من وجود المستخدم في جدول Supplier
                supplier = Supplier.query.get(current_user.id)
                if supplier:
                    user_type = 'supplier'
                    session['user_type'] = 'supplier'
                else:
                    return "❌ لا يمكن تحديد نوع المستخدم", 400
        
        # ✅ التحقق من وجود user_type
        if user_type not in ['supplier', 'staff']:
            return "❌ نوع المستخدم غير معروف", 400
        
        # ✅ جلب supplier_id بأمان
        if user_type == 'staff':
            supplier_id = getattr(current_user, 'supplier_id', None)
        else:
            supplier_id = current_user.id
        
        # ✅ التحقق من وجود supplier_id
        if not supplier_id:
            return "❌ لا يوجد مورد مرتبط بهذا الحساب", 404
        
        # ✅ جلب المورد
        supplier = db.session.get(Supplier, supplier_id)
        
        if not supplier:
            return "❌ المورد غير موجود", 404
        
        # ✅ جلب المحفظة
        wallet = SupplierWallet.query.filter_by(supplier_id=supplier.id).first()
        supplier.wallet = wallet
        
        # ✅ عدد الطلبات
        pending_orders_count = Order.query.filter_by(
            supplier_id=supplier.id, status='pending'
        ).count()
        
        # ✅ عرض القالب
        return render_template(
            'suppliers/dashboard.html',
            supplier=supplier,
            pending_orders_count=pending_orders_count,
            total_sales=0
        )
        
    except Exception as e:
        # ✅ عرض تفاصيل الخطأ كاملة
        error_details = traceback.format_exc()
        print(f"❌ خطأ في dashboard: {error_details}")
        
        return f"""
        <div style="direction: rtl; font-family: Tahoma; padding: 30px; text-align: center;">
            <h2 style="color: #d9534f;">❌ خطأ في لوحة التحكم</h2>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: right; margin: 20px auto; max-width: 800px; overflow: auto; border: 1px solid #ddd;">
                <p><strong>تفاصيل الخطأ:</strong></p>
                <pre style="background: #fff; padding: 15px; border-radius: 5px; border: 1px solid #ddd; font-size: 12px; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word;">{error_details}</pre>
            </div>
            <a href="/supplier/dashboard" style="background: #2d0b36; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px;">محاولة مرة أخرى</a>
        </div>
        """, 500


# ============================================================
# ✅ مساعد DeepSeek AI
# ============================================================
@suppliers_dashboard_bp.route('/api/ask-ai', methods=['POST'])
@login_required
def ask_ai():
    """
    واجهة API للتواصل مع DeepSeek AI
    """
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'السؤال مطلوب'
            }), 400
        
        # ✅ التحقق من وجود مفتاح API
        if not Config.DEEPSEEK_API_KEY:
            return jsonify({
                'success': False,
                'error': 'مفتاح DeepSeek غير موجود'
            }), 500
        
        # ✅ إرسال الطلب إلى DeepSeek
        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers={
                'Authorization': f'Bearer {Config.DEEPSEEK_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': Config.DEEPSEEK_MODEL,
                'messages': [
                    {
                        'role': 'system',
                        'content': """أنت مساعد ذكي لمتجر محجوب أونلاين. مهمتك مساعدة الموردين في:
1. تحسين مبيعاتهم
2. تسويق منتجاتهم
3. إدارة المخزون
4. فهم التحليلات
5. نصائح لتطوير المتجر
كن ودوداً، محترفاً، ومفيداً. استخدم اللغة العربية الفصحى."""
                    },
                    {
                        'role': 'user',
                        'content': question
                    }
                ],
                'max_tokens': Config.DEEPSEEK_MAX_TOKENS,
                'temperature': Config.DEEPSEEK_TEMPERATURE
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get('choices', [{}])[0].get('message', {}).get('content', 'عذراً، لم أستطع معالجة طلبك.')
            
            # ✅ تنظيف الإجابة
            answer = answer.strip()
            
            return jsonify({
                'success': True,
                'answer': answer
            })
        else:
            print(f"❌ خطأ في DeepSeek API: {response.status_code} - {response.text}")
            return jsonify({
                'success': False,
                'error': f'خطأ في الاتصال بالذكاء الاصطناعي'
            }), 500
            
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': 'انتهى وقت الانتظار، يرجى المحاولة مرة أخرى'
        }), 408
    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في طلب DeepSeek: {e}")
        return jsonify({
            'success': False,
            'error': 'حدث خطأ في الاتصال'
        }), 500
    except Exception as e:
        print(f"❌ خطأ غير متوقع في AI: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# coding: utf-8
from flask import Blueprint, request, jsonify
import logging

# إعداد السجلات (Logs) لتتمكن من رؤية البيانات في لوحة تحكم Render
logger = logging.getLogger(__name__)

# إنشاء Blueprint للويب هوك
webhooks_bp = Blueprint('webhooks', __name__)

@webhooks_bp.route('/api/webhooks/qumra', methods=['POST'])
def handle_qumra_webhook():
    # 1. استلام البيانات
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    # 2. طباعة البيانات للتحقق (ستظهر في سجلات Render)
    logger.info(f"✅ Webhook Received: {data}")
    
    # 3. الرد على المنصة
    return jsonify({"status": "success"}), 200

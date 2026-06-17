from flask import Blueprint, request, jsonify
import logging

# إعداد سجلات الخطأ لمراقبة ما يصل من المنصة
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

webhooks_bp = Blueprint('webhooks', __name__)

@webhooks_bp.route('/api/webhooks/qumra', methods=['POST'])
def handle_qumra_webhook():
    try:
        # استقبال البيانات كـ JSON
        data = request.get_json()
        
        if not data:
            logger.warning("Webhook received empty request")
            return jsonify({"error": "No data received"}), 400
        
        # تسجيل البيانات في الـ Logs لتتمكن من رؤيتها في Render
        logger.info(f"Received Qumra Webhook: {data}")
        
        # يمكنك هنا إضافة منطق المعالجة حسب نوع الحدث
        # مثال: event = data.get('event')
        
        return jsonify({"status": "received"}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

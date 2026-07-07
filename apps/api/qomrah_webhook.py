# coding: utf-8
import hashlib
import hmac
from flask import request, jsonify
from apps.extensions import db
from apps.api.sync_engine import SyncEngine
from config import Config

def verify_signature(payload, signature):
    """التحقق من أن الطلب قادم فعلاً من قمرة عبر HMAC."""
    expected_signature = hmac.new(
        Config.WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def handle_qomrah_webhook():
    signature = request.headers.get('X-Qomrah-Signature')
    payload = request.data

    # 1. التحقق الأمني
    if not verify_signature(payload, signature):
        return jsonify({"status": "error", "message": "Invalid signature"}), 403

    data = request.json
    order_id = data.get('order_id')
    
    # 2. هنا نقوم بطلب البيانات الكاملة باستخدام GraphQL
    # استدعاء دالة (سنتفق عليها) تجلب البيانات من رابط الـ GraphQL
    # full_order_data = QomrahClient.get_order_details(order_id)
    
    # 3. تمرير البيانات لمحرك المزامنة
    # success = SyncEngine.process_financials(
    #     order_id=full_order_data['id'],
    #     supplier_id=full_order_data['supplier_id'],
    #     total_price=full_order_data['total_price'],
    #     tracking_tag=full_order_data.get('tracking_tag')
    # )

    return jsonify({"status": "received", "order_id": order_id}), 200

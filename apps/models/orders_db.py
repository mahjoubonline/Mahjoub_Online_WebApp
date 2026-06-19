# coding: utf-8
from apps.extensions import db

class ProcessedOrder(db.Model):
    __tablename__ = 'processed_orders'
    id = db.Column(db.String(100), primary_key=True)
    order_id = db.Column(db.String(50))
    total_price = db.Column(db.Float)
    order_status = db.Column(db.String(50))
    customer_name = db.Column(db.String(100))
    customer_phone = db.Column(db.String(50))
    customer_email = db.Column(db.String(100))
    shipping_city = db.Column(db.String(100))
    shipping_street = db.Column(db.String(200))

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), db.ForeignKey('processed_orders.id'))
    product_title = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

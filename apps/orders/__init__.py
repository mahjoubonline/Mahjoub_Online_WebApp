from flask import Blueprint, render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # توجيه المستخدم مباشرة إلى لوحة التحكم أو الصفحة المطلوبة
    return redirect(url_for('orders.dashboard')) # تأكد أن هذا هو اسم المسار الصحيح للوحة التحكم

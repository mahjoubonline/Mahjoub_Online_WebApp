# coding: utf-8
from flask import Blueprint

# تعريف الـ Blueprint باسم 'wallet' ليتطابق مع ما تم تسجيله في apps/__init__.py
# وهذا هو الاسم الذي سيعتمد عليه url_for في القوالب
wallet_bp = Blueprint('wallet', __name__, template_folder='templates')

# استيراد الـ routes لضمان تسجيل المسارات داخل الـ Blueprint
from . import routes

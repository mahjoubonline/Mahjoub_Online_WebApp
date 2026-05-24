# coding: utf-8
# 📂 apps/wallet/__init__.py

from flask import Blueprint

# تأسيس المخطط المالي الحاكم بالاسم الموحد والمطابق للمصنع
wallet_blueprint = Blueprint(
    'wallet',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from apps.wallet import routes

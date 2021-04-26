from flask import Blueprint

account = Blueprint('account_app', __name__)

from . import account_view
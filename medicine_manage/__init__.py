from flask import Blueprint

medicine = Blueprint('medicine_app', __name__)

from . import medicine_view
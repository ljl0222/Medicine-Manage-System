from flask import Blueprint

prescription = Blueprint('prescription_app', __name__)

from . import prescription_view
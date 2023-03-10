from flask import Blueprint

six_jar_bp = Blueprint('six_jar', __name__)


from . import view
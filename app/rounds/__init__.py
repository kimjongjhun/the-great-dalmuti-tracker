from flask import Blueprint

rounds_bp = Blueprint("rounds_bp", __name__)

from app.rounds import routes
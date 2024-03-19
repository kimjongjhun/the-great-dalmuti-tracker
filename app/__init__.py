from flask import Flask
from flask_cors import CORS

def create_app():
  app = Flask(__name__)
  CORS(app)

  from app.rounds import rounds_bp
  app.register_blueprint(rounds_bp, url_prefix="/rounds")

  return app
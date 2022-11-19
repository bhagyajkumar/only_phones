from flask import Flask
from .ext import db, login_manager
from .models import User
from .routes import view
import os

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    app.register_blueprint(view)


    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    return app
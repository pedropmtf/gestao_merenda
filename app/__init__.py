from flask import Flask
from flask_bootstrap import Bootstrap
from app.models import db, login_manager

def create_app():
    app = Flask(__name__)
    
    Bootstrap(app)
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


    login_manager.init_app(app)

    from app import routes
    routes.init_app(app)

    return app



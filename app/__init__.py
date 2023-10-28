from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hello"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .routes import routes

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')
    
    with app.app_context():
        db.create_all()

    return app


def create_database(app):
    if not os.path.exists("app/" + DB_NAME):
        db.create_all(app=app)
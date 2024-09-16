from flask import Flask,session,redirect,url_for,render_template
#from flask_sqlalchemy import SQLAlchemy
from os import path
from .modles import User
#db=SQLAlchemy()
from flask_login import LoginManager
from .modles import db
from flask_socketio import join_room,leave_room,send,SocketIO


DB_NAME='database.db'
socketio=SocketIO()
def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY']='nanwn'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .view import views
    from .auth import auth

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
 
    from .modles import User,Note
    create_databse(app)
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    socketio.init_app(app)

    return app
def create_databse(app):
    if not path.exists('website/'+DB_NAME):
        with app.app_context():
            db.create_all()
        print("database created")





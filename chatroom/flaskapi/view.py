from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_socketio import emit
from flaskapi.init import socketio

views = Blueprint('views', __name__)

@views.route("/", methods=['POST', "GET"])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/room")
@login_required
def room():
    return render_template('room.html', user=current_user)


@socketio.on("connect")
def handle_connect():
    print(f"{current_user.first_name} has connected!")


@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message from {current_user.first_name}: {message}")
    emit("chat", {"message": message, "username": current_user.first_name}, broadcast=True)

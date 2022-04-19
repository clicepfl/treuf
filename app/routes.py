from flask import flash, redirect, render_template, request, url_for
from app import app, db
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    return render_template("index.html", title="Home")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    # TODO
    return ""


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    # TODO
    return ""


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    return render_template("user.html", user=user)

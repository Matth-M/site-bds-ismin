from flask import Blueprint, redirect, url_for

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return redirect(url_for("gym.planning"))

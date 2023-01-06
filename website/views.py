from flask import Blueprint, render_template

from website.db import get_db

views = Blueprint('views', __name__, url_prefix='/')


@views.route('/')
def home():
    return render_template("index.html")

@views.route('/calendar')
def calendar():
    # db = get_db()
    # reservations = db.execute(
    #         'SELECT r.id, user_id, time, username'
    #         ' FROM reservation r JOIN user u ON p.user_id = u.id'
    # ).fetchall()

    return render_template('calendar.html')

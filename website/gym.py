import datetime

from flask import Blueprint
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import flash
from flask import g
from dateutil.parser import parse
from sqlalchemy import select
from website.auth import login_required

from .models import db, Reservation, User

gym = Blueprint("gym", __name__, url_prefix="/gym")


@gym.route("/planning", methods=["GET"])
def planning():
    reservations = db.session.scalars(select(Reservation)).all()

    # Check if there are reservations made
    if reservations is None:
        reservations = []
    return render_template("gym_planning.html", reservations=reservations)


@gym.route("/create", methods=["POST"])
@login_required
def create():
    if request.method == "POST":
        # Get the reservation_time input by the user
        raw_reservation_time = request.form.get("time")
        reservation_time = parse(raw_reservation_time)

        # Check for incorrect input
        error = None

        # No input time
        if not reservation_time:
            error = "Time is required"

        # Input time is earlier than now
        elif reservation_time.utcnow() > datetime.datetime.utcnow():
            print(reservation_time.utcnow() < datetime.datetime.utcnow())
            error = "Please select a valid time"

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO reservation (time, user_id)" "VALUES (?, ?)",
                    (reservation_time, g.user["id"]),
                )
                db.commit()
            except db.IntegrityError:
                error = "Slot is already taken."
        flash(error)

    return redirect(url_for("gym.planning"))

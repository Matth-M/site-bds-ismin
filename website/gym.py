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

        reservation = db.session.scalars(
            select(Reservation).where(Reservation.time == reservation_time)
        ).first()

        # No input time
        if not reservation_time:
            error = "Time is required!"
        elif reservation is not None:
            error = "Slot is already taken!"

        # Input time is earlier than now
        elif reservation_time.utcnow() > datetime.datetime.utcnow():
            print(reservation_time.utcnow() < datetime.datetime.utcnow())
            error = "Please select a valid time"

        if error is None:
            user = g.user
            reservation = Reservation(
                time=reservation_time,
                user=user,
            )
            try:
                db.session.add(reservation)
                db.session.commit()
            except db.IntegrityError:
                error = "Slot is already taken."
        else:
            flash(error)

    return redirect(url_for("gym.planning"))


@gym.route("/delete/<int:reservation_id>", methods=["POST"])
@login_required
def delete(reservation_id):
    if request.method == "POST":
        # Fetch the reservation
        reservation = db.session.get(Reservation, reservation_id)
        error = None

        # No input time
        if not reservation:
            error = "No reservation found!"

        user = reservation.user

        if user != g.user:
            error = "You can't delete others reservation"

        if error is None:
            try:
                db.session.delete(reservation)
                db.session.commit()
            except db.IntegrityError:
                error = "Internal Error"
        else:
            flash(error)

    return redirect(url_for("gym.planning"))

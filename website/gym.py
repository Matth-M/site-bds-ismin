import datetime
import json

from flask import Blueprint
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import flash
from flask import g
from dateutil.parser import parse
from website.auth import login_required

from website.db import get_db

gym = Blueprint('gym', __name__, url_prefix='/gym')

@gym.route('/planning', methods=['GET'])
def planning():
    db = get_db()
    # Fetch all the reservations
    reservations = db.cursor().execute(
            'SELECT * FROM reservation'
    ).fetchall()

    # Convert Row objects into tuples so they can be serialized
    reservations = [tuple(row) for row in reservations]

    # reservations = [reservation.timestamp() for reservation in reservations]
    #
    # # Serialize the objects
    # reservations = json.dumps(reservations)

    return render_template('gym_planning.html', reservations=reservations)


@gym.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':

        # Get the reservation_time input by the user
        raw_reservation_time = request.form.get('time')
        reservation_time = parse(raw_reservation_time)
        print(f'raw_reservation_time {raw_reservation_time}')
        print(f'reservation_time: {reservation_time}')

        # Check for incorrect input
        error = None

        # No input time
        if not reservation_time:
            error = 'Time is required'

        # Input time is earlier than now
        elif reservation_time.utcnow() > datetime.datetime.utcnow():
            print(reservation_time.utcnow() < datetime.datetime.utcnow())
            error = 'Please select a valid time'

        # Insert data into the database
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO reservation (time, user_id)"
                "VALUES (?, ?)",
                (reservation_time, g.user['id'])
            )
            db.commit()


    return redirect(url_for('gym.planning'))

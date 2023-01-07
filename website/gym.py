from flask import Blueprint, render_template

from website.db import get_db

gym = Blueprint('gym', __name__, url_prefix='/gym')

@gym.route('/planning')
def planning():
    db = get_db()
    reservations = db.execute(
            'SELECT r.id, user_id, time, username'
            ' FROM reservation r JOIN user u ON r.user_id = u.id'
    ).fetchall()

    return render_template('gym_planning.html', reservations=reservations)

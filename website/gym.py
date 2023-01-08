from flask import Blueprint, render_template, request

from website.db import get_db

gym = Blueprint('gym', __name__, url_prefix='/gym')

@gym.route('/planning', methods=['GET', 'POST'])
def planning():
    db = get_db()
    reservations = db.execute(
            'SELECT r.id, user_id, time, username'
            ' FROM reservation r JOIN user u ON r.user_id = u.id'
    ).fetchall()

    if request.method == 'POST':
        date = request.form.get('time')
        print(date)

    return render_template('gym_planning.html', reservations=reservations)

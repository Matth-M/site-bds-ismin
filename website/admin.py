from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .models import Reservation, User
from .models import db


admin = Admin()


class UserView(ModelView):
    column_exclude_list = [
        "password",
    ]


class ReservationView(ModelView):
    column_list = [
        "time",
        "user.username",
    ]


admin.add_view(UserView(User, db.session))
admin.add_view(ReservationView(Reservation, db.session))

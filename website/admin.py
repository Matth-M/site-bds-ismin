from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers.response import Response

from .models import Reservation, User
from .models import db


basic_auth = BasicAuth()

admin = Admin()

"""
The following  classes are inherited from their respective base class,
and are customized, to make flask_admin compatible with BasicAuth.
"""


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(
            message,
            Response(
                "You could not be authenticated. Please refresh the page.",
                401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'},
            ),
        )


class UserView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException("Not authenticated.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return basic_auth.challenge()

    column_exclude_list = [
        "password",
    ]


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException("Not authenticated.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return basic_auth.challenge()


class ReservationView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException("Not authenticated.")
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return basic_auth.challenge()

    column_list = [
        "time",
        "user.username",
    ]


admin.add_view(UserView(User, db.session))
admin.add_view(ReservationView(Reservation, db.session))

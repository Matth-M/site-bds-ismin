import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from sqlalchemy import select

from werkzeug.security import check_password_hash, generate_password_hash

from website.models import User

from .models import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        email = request.form.get("email")
        password = request.form.get("password")
        error = None

        # Fetch user
        user = db.session.scalars(select(User).where(User.email == email)).first()

        # Check if user exists
        if user is None:
            error = "Incorrect email."
        elif not check_password_hash(user.password, str(password)):
            error = "Incorrect Password"

        # Add user info to the session
        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("views.index"))
        else:
            flash(error)

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("views.index"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if g.user is not None:
        return redirect(url_for("views.index"))

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password-confirm")

        error = None

        user = db.session.scalars(select(User).where(User.email == email)).first()

        if not username:
            error = "Username required."
        elif not password:
            error = "Password required"
        elif not email:
            error = "Email required"
        elif password != password_confirm:
            error = "Passwords don't match"
        elif user is not None:
            error = f"{email} is already taken!"

        if error is None:
            user = User(
                email=email,
                username=username,
                password=generate_password_hash(password),
            )
            try:
                db.session.add(user)
            except db.IntegrityError:
                error = f"{email} is already used."
            else:
                flash("User created successfully!")
                return redirect(url_for("auth.login"))

        flash(f"{error}")

    return render_template("sign_up.html")


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.scalars(select(User).where(User.id == user_id)).first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view

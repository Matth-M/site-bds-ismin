from flask import Blueprint, redirect, render_template, url_for, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        password_confirm = request.form.get('password-confirm')

        if len(email) < 5:
            flash('Email is too short.', category='error')
        elif password != password_confirm:
            flash('Passwords are not matching.', category='error')
        elif len(firstname) > 50:
            flash('Firstname is too long.', category='error')
        else:
            flash('Account created successfully!', category='success')

        # access database
    return render_template("sign_up.html")

from cs50 import SQL
from datetime import timedelta
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure Application
app =  Flask(__name__)
app.config['SECRET_KEY'] = 'X7TS4-3FX35-N1AQW-J90RT-F67NP'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)  # Set session lifetime to 7 day
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tasks.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")



''' User Authentication '''

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register the user"""

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Make sure user has provied all the required details
        if not username or not password or not confirm_password:
            flash("Please enter your details", "info")
            return redirect(request.referrer)

        # Validate username
        usernames = db.execute("SELECT id FROM users WHERE username = ?", username)

        if len(usernames) > 0:
            flash("Username already exists!", "info")
            return redirect(request.referrer)

        # Validate passwords
        if password != confirm_password:
            flash("Password did not matched!", "info")
            return redirect(request.referrer)

        # Hash the password
        password = generate_password_hash(password)

        # Add the user to database
        db.execute("INSERT INTO users(username, password) VALUES(?, ?)", username, password)

        users = db.execute("SELECT id FROM users WHERE username = ?", username)

        # Clear session and session for current user
        session.clear()
        session['user_id'] = users[0]['id']

        flash("Account created successfully!", "success")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login the user"""

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Please enter your details!", "info")
            return redirect(request.referrer)

        # Check if username exists and password is correct
        users = db.execute("SELECT id, password FROM users WHERE username = ?", username)

        if not len(users) == 1 or not check_password_hash(users[0]['password'], password):
            flash("Invalid username/password!", "danger")
            return redirect(request.referrer)

        # Add the user to session
        session.clear()
        session['user_id'] = users[0][id]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout the user"""
    session.clear()
    flash("You have been logged out!", "info")
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)

from flask import (
    flash,
    redirect,
    render_template,
    url_for,
    request,
    session,
    g,
    Blueprint,
)

from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

from finance.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        )


@bp.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Endpoints
@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not confirmation:
            error = "Confirmation is required."
        elif not password == confirmation:
            error = "Confirmation did not match with the password."

        if error is None:
            # Add user to database
            try:
                db.execute(
                    "INSERT INTO users (username, hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # Success
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    db = get_db()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if username == "":
            error = "Username is required."
        elif password == "":
            error = "Password is required."

        if error is None:
            rows = db.execute(
                "SELECT * FROM users WHERE username = ?",
                (request.form.get("username"),),
            ).fetchall()

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"], request.form.get("password")
            ):
                error = "Invalid username and/or password."
            else:
                session["user_id"] = rows[0]["id"]
                return redirect("/")

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

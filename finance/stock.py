from flask import flash, render_template, request, Blueprint

from finance.helpers import apology, lookup
from finance.auth import login_required

bp = Blueprint("stock", __name__)


@bp.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("stock/index.html")


@bp.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@bp.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@bp.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    quote = None

    if request.method == "POST":
        symbol = request.form.get("qSymbol")
        quote = lookup(symbol)
        error = None

        if symbol == "":
            error = "Symbol for quote is required."
        elif quote is None:
            error = "Invalid symbol for quote."

        flash(error)

    return render_template("stock/quote.html", quote=quote)


@bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")

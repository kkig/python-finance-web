from flask import render_template, request, Blueprint

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

        if symbol is None:
            return apology("Symbol for quote is required.")

        quote = lookup(symbol)
        print(quote)
        if quote is None:
            return apology("Invalid symbol for quote.")

    return render_template("stock/quote.html", quote=quote)


@bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")

from flask import flash, redirect, render_template, request, session, Blueprint

from finance.helpers import apology, lookup, usd
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
    return apology("TODO")


@bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")

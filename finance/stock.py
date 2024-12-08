from flask import flash, render_template, url_for, redirect, request, g, Blueprint
import sqlite3
from werkzeug.exceptions import abort

from finance.helpers import apology, lookup, usd

from finance.auth import login_required
from finance.db import get_db

bp = Blueprint("stock", __name__)


@bp.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def get_stock_total(id):
    """Get counts of stock per symbol."""
    db = get_db()
    data = db.execute(
        "SELECT SUM(shares) as [total_shares], symbol FROM transactions"
        "   WHERE user_id = (?) GROUP BY symbol",
        (id,),
    ).fetchall()

    total, stocks = 0, []

    for item in data:
        curr = lookup(item["symbol"])
        cur_total = item["total_shares"] * curr["price"]
        total += cur_total

        stocks.append(
            {
                "symbol": item["symbol"],
                "shares": item["total_shares"],
                "price": usd(curr["price"]),
                "total": usd(cur_total),
            }
        )

    return {"total": total, "stocks": stocks}


@bp.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    data = get_stock_total(g.user["id"])
    data["cash"] = usd(g.user["cash"])
    data["total"] = usd(data["total"] + g.user["cash"])

    return render_template(
        "stock/index.html",
        data=data,
    )


@bp.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        db, quote, error = get_db(), None, None

        if not symbol or not shares:
            error = "Missing symbol." if not symbol else "Missing shares."
        elif not shares.isnumeric():
            error = "Invalid value for shares."
        else:
            quote = lookup(symbol)
            error = None if quote else "Invalid symbol."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO transactions (user_id, symbol, shares, price)"
                    "   VALUES (?, ?, ?, ?)",
                    (
                        g.user["id"],
                        symbol,
                        int(shares),
                        quote["price"],
                    ),
                )
                db.commit()
            except sqlite3.Error as e:
                # Error inserting data
                error = e.sqlite_errorname
                print(error)
            else:
                # Success
                return redirect(url_for("stock.index"))

        flash(error)

    return render_template("stock/buy.html")


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
        symbol = request.form.get("symbol")
        quote = None
        error = None

        if symbol == "":
            error = "Symbol for quote is required."
        else:
            quote = lookup(symbol)
            error = None if quote else "Invalid symbol for quote."

        flash(error)

    return render_template("stock/quote.html", quote=quote)


@bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")

from flask import flash, render_template, url_for, redirect, request, g, Blueprint

from finance.helpers import apology, lookup, usd

from finance.auth import login_required
from finance.db import database

bp = Blueprint("stock", __name__)


@bp.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def get_stock_total(user_id):
    """Get counts of stock per symbol."""
    db = database()
    shares_list = db.get("shares", user_id)
    if len(shares_list) == 0:
        return None

    total, stocks = 0, []

    for stock in shares_list:
        price = lookup(stock["symbol"])["price"]
        cur_total = stock["shares"] * price
        total += cur_total

        stocks.append(
            {
                "symbol": stock["symbol"],
                "shares": stock["shares"],
                "price": usd(price),
                "total": usd(cur_total),
            }
        )

    return {"total": total, "stocks": stocks}


@bp.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id, cash = g.user["id"], g.user["cash"]
    total, stocks = cash, None

    shares_list = get_stock_total(user_id)

    if shares_list:
        total += shares_list["total"]
        stocks = shares_list["stocks"]

    return render_template(
        "stock/index.html",
        total=usd(total),
        cash=usd(cash),
        stocks=stocks,
    )


@bp.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Validate inputs
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        error = None

        if not symbol or not shares:
            error = "Symbol and shares are required."

        # Check if input is valid
        db, quote = database(), None

        if error is None:
            quote = lookup(symbol)
            if not symbol.isalpha() or not shares.isnumeric():
                error = "Invalid value for Symbol or Shares."
            elif quote is None:
                error = "Invalid symbol."

        # Check if there is enogh cash to buy
        user_id, cash = g.user["id"], g.user["cash"]
        price, cash_remain = None, cash

        if error is None:
            price = quote["price"]
            cash_remain -= int(shares) * price
            if cash_remain <= 0:
                error = "Not enough cash to buy."

        # Update database for valid input.
        if error is None:
            db.update("cash", user_id, cash_remain)

            data = {"id": user_id, "symbol": symbol, "shares": shares, "price": price}
            db.insert("trans", **data)

            # Update global variable
            g.pop("user", None)
            g.user = db.get("user", user_id)

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

        if error:
            flash(error)

    return render_template("stock/quote.html", quote=quote)


@bp.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")

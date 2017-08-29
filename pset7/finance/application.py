from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")
        # ensure username was submitted
        if username and password and password_confirmation and (password == password_confirmation):

            # query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

            # ensure username exists and password is correct
            if len(rows) > 0:
                return apology("username already exists")
            else:
                result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", 
                    username=username, hash=pwd_context.hash(password)
                    )
                if result:
                    # remember which user has logged in
                    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
                    session["user_id"] = rows[0]["id"]

                    return redirect(url_for("index"))
                else:
                    return apology("Sorry, something went wrong!")
        else:
            return apology("Must provide username AND password AND password confirmation")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT * FROM user_stocks WHERE user_id = :user_id", user_id=session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])[0]
    stock_current_prices = {}
    total_stock_values = 0
    for row in rows:
        stock = lookup(row["name"])
        stock_current_prices[stock["symbol"]] = stock["price"]
        total_stock_values += stock["price"] * row["quantity"]
    return render_template("index.html", user_stocks=rows, user=user, stock_current_prices=stock_current_prices, total_stock_values=total_stock_values)

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        quote = lookup(request.form.get("symbol"))

        if quote != None:
            return render_template("stock_info.html", name=quote["name"], price=quote["price"], symbol=quote["symbol"])
        else:
            return apology("Could not find the stock, please try again")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "GET":
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        return render_template("buy.html", user_cash=rows[0]["cash"])
    else:
        quote = lookup(request.form.get("symbol"))
        number_of_shares = int(request.form.get("number_of_shares"))

        if quote and quote["price"] and quote["symbol"] and number_of_shares:
            user = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])[0]
            user_cash = user["cash"]
            total_stock_price = quote["price"] * number_of_shares
            
            if total_stock_price > user_cash:
                return apology("Sorry, you can not afford this, man.")
            else:
                user_cash -= total_stock_price
                
                db.execute("INSERT INTO user_transactions (user_id, stock, quantity, price) VALUES(:user_id, :stock, :quantity, :price)", 
                    user_id=user["id"], stock=quote["symbol"], quantity=number_of_shares, price=quote["price"])
                rows = db.execute("SELECT * FROM user_stocks WHERE user_id = :user_id AND name = :name", user_id=user["id"], name=quote["symbol"])
                if len(rows) > 0:
                    db.execute("UPDATE user_stocks SET quantity = :quantity WHERE id = :id", quantity=rows[0]["quantity"] + number_of_shares, id=rows[0]["id"])
                else:
                    db.execute("INSERT INTO user_stocks (user_id, name, quantity, price) VALUES(:user_id, :name, :quantity, :price)", 
                        user_id=user["id"], name=quote["symbol"], quantity=number_of_shares, price=quote["price"])
                db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=user_cash, id=user["id"])

                return redirect(url_for("index"))
        else:
            return apology("Please enter symbol of the stock and number of shares you want to buy")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "GET":
        user_stocks = db.execute("SELECT name FROM user_stocks WHERE user_id = :user_id", user_id=session["user_id"])
        return render_template("sell.html", user_stocks=user_stocks)
    else:
        quantity = int(request.form.get("quantity"))
        stock = lookup(request.form.get("stock_name"))
        if  quantity and stock and stock["symbol"] and stock["price"]:
            rows = db.execute("SELECT * FROM user_stocks WHERE user_id = :user_id AND name = :name", user_id=session["user_id"], name=stock["symbol"])
            if len(rows) > 0 and rows[0]["quantity"] >= quantity:
                db.execute("INSERT INTO user_transactions (user_id, stock, quantity, price) VALUES(:user_id, :stock, :quantity, :price)", 
                    user_id=session["user_id"], stock=stock["symbol"], quantity=quantity, price=-stock["price"])
                updated_quantity = rows[0]["quantity"] - quantity
                db.execute("UPDATE user_stocks SET quantity = :quantity WHERE user_id = :user_id AND name = :name", 
                    user_id=session["user_id"], name=stock["symbol"], quantity=updated_quantity)
                revenue = stock["price"] * quantity
                db.execute("UPDATE users SET cash = cash + :revenue WHERE id = :id", revenue=revenue, id=session["user_id"])
                return redirect(url_for("index"))
            else:
                return apology("You don't have enough shares to sell")
        else:
            return apology("You must provide stock name and quantity")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    transactions = db.execute("SELECT * FROM user_transactions WHERE user_id = :user_id ORDER BY created_at DESC", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)
    

@app.route("/add_cash", methods=["POST"])
@login_required
def add_cash():
    """Add cash for logged in user"""
    amount = int(request.form.get("amount"))
    if amount and amount > 0:
        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :id", amount=amount, id=session["user_id"])
        return redirect(url_for("index"))
    else:
        return apology("Please type a positive number for the amount you want to save")
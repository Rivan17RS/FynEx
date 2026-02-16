from flask import Flask, render_template, request, redirect, session
from decimal import Decimal, ROUND_HALF_UP
import database
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"

database.init_db()


def get_exchange_rate():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=5)
        data = response.json()
        return Decimal(str(data["rates"]["CRC"]))
    except:
        return Decimal("520")  # fallback rate


@app.route("/")
def index():
    currency = session.get("currency", "CRC")
    rate = get_exchange_rate()

    expenses = database.fetch_expenses()
    balance = Decimal(str(database.get_total_balance()))
    monthly = database.get_monthly_summary()
    categories = database.get_category_distribution()

    if currency == "CRC":
        balance = (balance * rate).quantize(Decimal("0.01"), ROUND_HALF_UP)

        expenses = [
            (
                e[0],
                e[1],
                e[2],
                float((Decimal(str(e[3])) * rate).quantize(Decimal("0.01"), ROUND_HALF_UP)),
                e[4],
            )
            for e in expenses
        ]

        categories = [
            (
                c[0],
                float((Decimal(str(c[1])) * rate).quantize(Decimal("0.01"), ROUND_HALF_UP)),
            )
            for c in categories
        ]

        monthly = [
            (
                m[0],
                float((Decimal(str(m[1])) * rate).quantize(Decimal("0.01"), ROUND_HALF_UP)),
            )
            for m in monthly
        ]

    return render_template(
        "index.html",
        expenses=expenses,
        balance=float(balance),
        monthly=monthly,
        categories=categories,
        currency=currency,
        rate=float(rate)
    )


@app.route("/add", methods=["POST"])
def add():
    date = request.form["date"]
    category = request.form["category"]
    amount = Decimal(request.form["amount"])
    description = request.form["description"]

    currency = session.get("currency", "CRC")
    rate = get_exchange_rate()

    # Convert to USD before storing
    if currency == "CRC":
        amount = (amount / rate).quantize(Decimal("0.01"), ROUND_HALF_UP)

    database.add_expense(date, category, float(amount), description)

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    database.delete_expense(id)
    return redirect("/")


@app.route("/toggle_currency")
def toggle_currency():
    current = session.get("currency", "CRC")

    if current == "CRC":
        session["currency"] = "USD"
    else:
        session["currency"] = "CRC"

    return redirect("/")

# Assigning port for RENDER
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

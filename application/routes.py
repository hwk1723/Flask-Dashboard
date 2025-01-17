from application import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.form import UserInputForm
from application.models import IncomeExpenses
import json

@app.before_request
def create_tables():
    # The following line will remove this handler, making it
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)

    db.create_all()

@app.route("/")
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template("index.html", title='index', entries=entries)

@app.route("/add", methods=['GET', 'POST'])
def add_expense():
    form = UserInputForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type = form.type.data, 
                               category = form.category.data, 
                               amount = form.amount.data)
        db.session.add(entry)
        db.session.commit()
        flash('Expense added successfully', 'success')
        return redirect(url_for('index'))
    return render_template("add.html", title = 'add', form = form)

@app.route("/delete/<int:entry_id>")
def delete_expense(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash('Expense deleted successfully', 'success')
    return redirect(url_for('index'))

@app.route("/dashboard")
def dashboard():
    income_vs_expense = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    category_vs_amount = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_labels = []
    for amount, date in dates:
        over_time_expenditure.append(amount)
        dates_labels.append(date.strftime('%m-%d-%Y'))

    category_amount = []
    for total_amount, _ in category_vs_amount:
        category_amount.append(total_amount)

    return render_template("dashboard.html", 
                           income_vs_expenses=json.dumps(income_expense), 
                           over_time_expenditure=json.dumps(over_time_expenditure), 
                           dates_label=json.dumps(dates_labels),
                           category_vs_amounts=json.dumps(category_amount))
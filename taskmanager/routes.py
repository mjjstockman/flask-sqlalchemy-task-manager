from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


@app.route("/")
def home():
    return render_template("tasks.html")


@app.route("/categories")
def categories():
    return render_template("categories.html")


# normal method used is GET, but uses POST when submitting form
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    # ie. form is being submitted
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        # add the data from db
        db.session.add(category)
        # commit data from db
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")
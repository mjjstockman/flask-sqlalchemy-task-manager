from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


@app.route("/")
def home():
    return render_template("tasks.html")


@app.route("/categories")
def categories():
    # query catagories model that's imported from models.py using the category_name key
    # .all() must be at end of query. returns a cursor obj (like an array) even
    # if only one obj. therefore wrap query in a list method
    categories = list(Category.query.order_by(Category.category_name).all())
    # 1st categories decleration is var name taken from html, 2nd is the catagories
    # var created above (the list of the cursor)
    return render_template("categories.html", categories=categories)


# normal method used is GET, but uses POST when submitting form
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        # ie. form is being submitted
        category = Category(category_name=request.form.get("category_name"))
        # add the data from db
        db.session.add(category)
        # commit data from db
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")
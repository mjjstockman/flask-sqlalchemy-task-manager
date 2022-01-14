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
    # ie. form is being submitted
    if request.method == "POST":
        # query the table using this category_name, store in category var
        category = Category(category_name=request.form.get("category_name"))
        # add the data to the session
        db.session.add(category)
        # commit the data to the db
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")


# angle brackets to use the arg category_id. all PK's so will be int's
@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
# pass category_id as param for function
def edit_category(category_id):
    # if can't find the category_id will trigger 404 error
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))

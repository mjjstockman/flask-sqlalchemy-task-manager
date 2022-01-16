from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


@app.route("/")
def home():
    # use imported Task model to query all tasks found and convert to list
    tasks = list(Task.query.order_by(Task.id).all())
    # pass the tasks to the template
    return render_template("tasks.html", tasks=tasks)


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


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    # query the table using this category_name to get all cataogory names
    #  from db, store in var called category
    categories = list(Category.query.order_by(Category.category_name).all())
    # can check models to see task schema (ie. needs name, descrition etc)
    if request.method == "POST":
        # using POST method as form info is being sent
        # create task var which hold all the info sent from the form fields
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            category_id=request.form.get("category_id")
        )
        # add the data to the session
        db.session.add(task)
        # commit the data to the db
        db.session.commit()
        # if all good, return user to home page
        return redirect(url_for("home"))
    # if method not POST, show the add_task page and send the categories as a param
    return render_template("add_task.html", categories=categories)


@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = bool(True if request.form.get("is_urgent") else False)
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")
        db.session.commit()
    return render_template("edit_task.html", task=task, categories=categories)


@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))


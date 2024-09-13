from flask import Flask, render_template, request, redirect, url_for
from mongoengine import connect, Document, StringField, BooleanField

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")

connection_string = "mongodb://localhost:27017"

connect(db='TodoAppDB', host=connection_string)

class Todo(Document):
    title = StringField(required=True)
    complete = BooleanField()

    meta = {
        "collection": "Todos"
    }

@app.get("/")
def home():
    try:
        abc = Todo.objects.get(title="sdf")
        print(abc)
    except:
        pass
    todo_list = Todo.objects.all()
    todo_list = reversed(todo_list)
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    new_todo.save()
    return redirect(url_for("home"))


@app.get("/update/<string:todo_id>")
def update(todo_id):
    try:
        todo = Todo.objects.filter(id=todo_id).first()
        todo.complete = not todo.complete
        todo.save()
    except:
        pass
    return redirect(url_for("home"))


@app.get("/delete/<string:todo_id>")
def delete(todo_id):
    try:
        todo = Todo.objects.filter(id=todo_id).first()
        todo.delete()
    except:
        pass
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True, port=5820)

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import shutil

app = Flask(__name__)

# /// = relative path, //// = absolute path
# connection_string = "postgresql://postgres:862830@localhost:5432/postgres"
connection_string = "postgresql://retool:Ls0kBhSbYe7j@ep-red-butterfly-a6r5zdsm.us-west-2.retooldb.com/retool?sslmode=require"

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

@app.get("/")
def home():
    todo_list = db.session.query(Todo).all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/disk")
def freedisk():
    total, used, free = shutil.disk_usage('/')
    stat = {
        "Total": f"{total / (2**30):.2f} GB",
        "Used": f"{used / (2**30):.2f} GB",
        "Free": f"{free / (2**30):.2f} GB",
    }
    return jsonify(stat)

@app.get("/write")
def writedisk():
    try:
        x = []
        for i in 20000:
            x.append(i)
        with open("./asdf.txt", "a") as f:
            f.write("x")
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

from flask.templating import render_template
from demo import app


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.j2")

@app.route("/about")
def about():
    return render_template("about.j2")

@app.route("/users")
def users():
    data = [
        {'id' : 1, 'name' : 'test1'},
        {'id' : 2, 'name' : 'test2'},
        {'id' : 3, 'name' : 'test3'},
    ]
    return render_template('users.html.j2', users=data, userName="TestName")

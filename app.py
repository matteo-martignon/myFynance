from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sayhello")
def sayHello():
    return render_template("sayHello.html")


@app.route("/<name>")
def hello_name(name):
    return f"Hello {name}!"


@app.route("/guest/<name>")
def hello_guest(name):
    return redirect(url_for("hello_name", name=name))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["Name"]
        return redirect(url_for("hello_name", name=user))
    elif request.method == "GET":
        user = request.args.get("Name")
        return redirect(url_for("hello_name", name=user))


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        result = request.form
        return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)

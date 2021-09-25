from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

# print(__name__)


@app.route("/")
def index():
    return render_template("hello.html")
# def index():
#     str="""
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Hello world</title>
# </head>
# <body>
#     <h1>Hello world</h1>
# </body>
# </html>
# """
#     return str
# def hello_world():
#     return "Hello!"


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


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, redirect, url_for

app = Flask(__name__)

print(__name__)


@app.route("/hello")
def hello_world():
    return "Hello!"

@app.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}!"


@app.route("/guest/<name>")
def hello_guest(name):
    return redirect(url_for("hello_name", name=name))


if __name__ == "__main__":
    app.run(debug=True)

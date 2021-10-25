from flask import Flask, redirect, url_for, request, render_template,\
    make_response, session, abort, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "random string"

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
        if request.form["Name"] != "neo":
            # or request.form["password"] != "morpheus":
            # error = "Invalid username or password. Please try again!"
            abort(401)
        else:
            # flash("You were successfully logged in")
            # flash("log out before login again")
            user = request.form["Name"]
            return redirect(url_for("hello_name", name=user))
            # return redirect(url_for("index"))
    elif request.method == "GET":
        user = request.args.get("Name")
        return redirect(url_for("hello_name", name=user))
    else:
        return "Failed"
    # return render_template("log_in.html", error=error)


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        result = request.form
        return render_template("result.html", result=result)


@app.route("/setcookie", methods=["POST", "GET"])
def set_cookie():
    if request.method == "POST":
        user = request.form["nm"]
        resp = make_response(render_template("readcookie.html"))
        resp.set_cookie("userID", value=user)
        return resp


@app.route("/getcookie")
def get_cookie():
    name = request.cookies.get("userID")
    # name = request.cookies.get("ajs_user_id")
    return f"<h1>Welcome {name}</h1>"


@app.route("/session")
def session_func():
    if "username" in session:
        username = session["username"]
        return f"Logged as {username}<br>" \
               f"<b><a href='/logout'>click here to log out</a></b>"
    return f"You are not logged in<br>" \
               f"<b><a href='/sessionlogin'>click here to log in</a></b>"


@app.route("/sessionlogin", methods=["POST", "GET"])
def session_login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("session_func"))
    return render_template("session.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("session_func"))


@app.route("/login2", methods=["POST", "GET"])
def login2():
    error = None
    if request.method == "POST":
        if request.form["username"] != "neo" or request.form["password"] != "morpheus":
            error = "Invalid username or password. Please try again!"
        else:
            flash("You were successfully logged in")
            flash("log out before login again")
            return redirect(url_for("index"))
    return render_template("log_in.html", error=error)


@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/uploader", methods=["POST", "GET"])
def uploader():
    if request.method == "POST":
        f = request.files["file"]
        f.save(secure_filename(f.filename))
        return f"File {f.filename} uploaded successfully"


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "jobportal123"

# upload folder create
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

jobs = [
    {"title":"Frontend Developer","company":"Google","location":"Bangalore","salary":"₹12 LPA"},
    {"title":"UI/UX Designer","company":"Adobe","location":"Hyderabad","salary":"₹10 LPA"},
    {"title":"Data Analyst","company":"Amazon","location":"Remote","salary":"₹11 LPA"},
    {"title":"Backend Developer","company":"Microsoft","location":"Pune","salary":"₹13 LPA"}
]

users = []

@app.route("/")
def home():
    search = request.args.get("search")

    if search:
        filtered = [j for j in jobs if search.lower() in j["title"].lower()]
    else:
        filtered = jobs

    return render_template("index.html", jobs=filtered)


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        for u in users:
            if u["username"] == username and u["password"] == password:
                session["user"] = username
                return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users.append({"username":username,"password":password})
        return redirect("/login")

    return render_template("register.html")


@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("resume")

        if file and file.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

    return render_template("upload.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


# important for render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask,render_template,request,redirect,session
import os

app = Flask(__name__)
app.secret_key="secret"

jobs = [
{"title":"Python Developer","company":"TechSoft","location":"Hyderabad"},
{"title":"Web Developer","company":"CodeLabs","location":"Bangalore"},
{"title":"Software Engineer","company":"Infosys","location":"Chennai"}
]

users=[]

UPLOAD_FOLDER="static/images"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():

    search=request.args.get("search")

    if search:
        filtered=[j for j in jobs if search.lower() in j["title"].lower()]
    else:
        filtered=jobs

    return render_template("index.html",jobs=filtered)

@app.route("/register",methods=["GET","POST"])
def register():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        users.append({"username":username,"password":password})

        return redirect("/login")

    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        for u in users:
            if u["username"]==username and u["password"]==password:
                session["user"]=username
                return redirect("/")

    return render_template("login.html")

@app.route("/upload",methods=["GET","POST"])
def upload():

    if request.method=="POST":

        file=request.files["resume"]

        if file:
            file.save(os.path.join(UPLOAD_FOLDER,file.filename))

    return render_template("upload.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

if __name__=="__main__":
    app.run()
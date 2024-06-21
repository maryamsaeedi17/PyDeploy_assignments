import os
import numpy as np
import cv2
from flask import Flask, render_template, request, redirect, url_for, session
# from deepface import DeepFace
# import tensorflow as tf
from sqlmodel  import Field, SQLModel, create_engine, Session, select
from pydantic import BaseModel

app = Flask("Analyze Face")
app.config["UPLOAD_FOLDER"] = './uploads'
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    city: str = Field()
    username:  str = Field()
    password: str = Field()

engine = create_engine('sqlite:///./database.db', echo=True)
SQLModel.metadata.create_all(engine)

# PyDantic models for request validation
class RegisterModel(BaseModel):
    city: str
    username: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str


def auth(email, password):
    if email == "maryam@maryam.saeedi" and password == "2468":
        return True
    else:
        return False
    
def allowed_file(filename):
    return True
    

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        try:
            login_model = LoginModel(
                username = request.form["username"],
                password = request.form["password"]
            )
        except:
            print("Type error")
            return redirect(url_for("login"))
        
        with Session(engine) as db_session:
            statement = select(User).where(User.username == login_model.username).where(User.password == login_model.password)
            result = db_session.exec(statement).first()   

        if result:
            print("Welcome, you are logged in")
            return redirect(url_for("upload"))
        else:
            print("Username or password is incorrect")
            return redirect(url_for("login"))
        

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        try:
            register_data = RegisterModel(
                city=request.form["city"], 
                username=request.form["username"], 
                password=request.form["password"])
        except:
            print("Type error")
            return redirect(url_for("register"))

        with Session(engine) as db_session:
            statement = select(User).where(User.username == register_data.username)
            result = db_session.exec(statement).first()

        if not result:
            with Session(engine) as db_session:
                user = User(
                    city=register_data.city,
                    username=register_data.username,
                    password=register_data.password
                )
                db_session.add(user)
                db_session.commit()
            print("your register done successfully")
            return redirect(url_for("login"))
        else:
            print("Username already exist, try another username")
            return redirect(url_for("register"))


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "GET":
        return(render_template("upload.html"))
    elif request.method == "POST":


        my_image = request.files['image']
        if my_image.filename == "":
            return redirect(url_for("upload"))
        else:
            if my_image and allowed_file(my_image.filename):
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], my_image.filename)
                my_image.save(save_path)
                
                color_img = cv2.imread(save_path)
                gray_img = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)
                cv2.imwrite("static/images/gray_image.jpg", gray_img)
                # result = DeepFace.analyze(
                #     img_path = "save_path",
                #     actions = ['age']
                # )
                # age = result[0]["age"]
            return redirect(url_for("result"))


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/bmr", methods=['GET', 'POST'])
def calculate_BMR():
    if request.method == "GET":
        return render_template("bmr.html")
    
    elif request.method == "POST":
        weight = int(request.form["weight"])
        height = int(request.form["height"])
        age = int(request.form["age"])
        gender = request.form["gender"]
        
        if gender == "female":
            bmr = (10*weight)+(6.25*height)-(5*age)-161
        elif gender == "male":
            bmr = (10*weight)+(6.25*height)-(5*age)+5

        return render_template("calculate.html", BMR=bmr)
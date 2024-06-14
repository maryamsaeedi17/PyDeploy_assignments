import os
import numpy as np
import cv2
from flask import Flask, render_template, request, redirect, url_for, session
# from deepface import DeepFace
# import tensorflow as tf


app = Flask("Analyze Face")
app.config["UPLOAD_FOLDER"] = './uploads'
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}


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
        my_emil = request.form["email"]
        my_password = request.form["password"]
        result = auth(my_emil, my_password)
        if result:
            return redirect(url_for("upload"))
        else:
            return redirect(url_for("login"))


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
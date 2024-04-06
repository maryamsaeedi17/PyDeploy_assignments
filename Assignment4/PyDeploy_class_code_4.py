from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import io

app = FastAPI()
friends={}

@app.get("/")
def read_root():
    return{"Hello": "World"}

@app.get("/items")
def read_friends():
    return friends

@app.post("/items")
def add_friends(id: str = Form(), name: str = Form(), age: float = Form()):
    friends[id]={"name": name, "age": age}
    return friends[id]


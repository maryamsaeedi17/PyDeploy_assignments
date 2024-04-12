from fastapi import FastAPI , Form , File , UploadFile , HTTPException
from fastapi.responses import StreamingResponse , FileResponse
import sqlite3
from database import Database


app = FastAPI()
db = Database()

@app.get("/read_database")
def read_database():
    ...

@app.post("/add_task/{id}/{title}/{description}/{time}/{status}")
def add_task():
    ...

@app.put("/update_task")
def update_db():
    ...

@app.delete("/remove_task/{id}")
def remove_task():
    ...
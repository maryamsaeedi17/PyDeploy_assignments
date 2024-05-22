from fastapi import FastAPI , Form , File , UploadFile , HTTPException
from fastapi.responses import StreamingResponse , FileResponse
import sqlite3

app = FastAPI()

def db_contents(cursor):
    con = sqlite3.connect("todo.db")
    cursor = con.cursor()
    db_content= []
    query = "SELECT id, title , description , time , status from TASKS"
    tasks = cursor.execute(query)
    for task in tasks:
        db_content.append({"id" : f"{task[0]}" , "title": f"{task[1]}" , "description": f"{task[2]}", "time": f"{task[3]}", "status": f"{task[4]}"})
    return db_content


@app.get("/read_database")
def read_database():
    con = sqlite3.connect("todo.db")
    cursor = con.cursor()
    database = db_contents(cursor)
    con.close()
    return database


@app.post("/add_task")
def add_task(title:str= Form(None) , description:str= Form(None) , time:str= Form(None) , status:int= Form(None)):
    con = sqlite3.connect("todo.db")
    cursor = con.cursor()
    query = query=f"INSERT INTO tasks(title, description, time) VALUES ('{title}', '{description}', '{time}')"
    cursor.execute(query) 
    con.commit()
    database = db_contents(cursor)
    con.close()
    return database
    
################################

@app.put("/update_task/{id}")
def update_task(id:int , field:str= Form(None) , value:str= Form(None)):
    con = sqlite3.connect("todo.db")
    cursor = con.cursor()
    query = f"SELECT * FROM TASKS WHERE id ={id}"
    result = cursor.execute(query)
    tasks = result.fetchall()
    if  len(tasks) < 1 :
        raise HTTPException(status_code=400 , detail="This ID does not exist in the database!!")        
    else :
        query = f"UPDATE TASKS SET {field} = '{value}' WHERE id = {id}"
        cursor.execute(query)
        con.commit()
        database = db_contents(cursor)
        con.close()
        return database


@app.delete("/delete_task/{id}")
def delete_task(id:int):
    con = sqlite3.connect("todo.db")
    cursor = con.cursor()
    query = f"SELECT * from TASKS WHERE id = {id}"
    cursor.execute(query)
    result = cursor.execute(query)
    tasks = result.fetchall()
    if len(tasks) == 0 :
        raise HTTPException(status_code=400 , detail="This ID does not exist in the database!!")
    else :
        query = f"DELETE from TASKS WHERE id = {id}"
        cursor.execute(query)
        con.commit()
        database = db_contents(cursor)
        con.close()
        return database
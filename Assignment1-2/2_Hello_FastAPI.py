from fastapi import FastAPI

app = FastAPI()

@app.get("/Maryam")
def read_root():
    return {"Hello" : "World"}


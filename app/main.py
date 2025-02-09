from fastapi import FastAPI, Depends
from db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root_read():
    return {"messages": "Hello World!"}
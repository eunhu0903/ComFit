from fastapi import FastAPI
from db.session import Base, engine
from api import user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def root_read():
    return {"messages": "Hello World!"}
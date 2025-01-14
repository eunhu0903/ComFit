from fastapi import FastAPI
from db.database import Base, engine
from routers import auth, workout, profile

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(workout.router)
app.include_router(profile.router)

@app.get("/")
def read_root():
    return {"message": "Hello World!"}
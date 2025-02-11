from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.session import Base, engine
from api import user, commit, home, profile

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(commit.router)
app.include_router(home.router)
app.include_router(profile.router)
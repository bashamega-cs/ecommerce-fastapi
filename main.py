from fastapi import FastAPI
from models import Base
from database import engine
from routers import items
from routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Ecommerce API"}

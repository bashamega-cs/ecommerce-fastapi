from fastapi import FastAPI
from models import Base
from database import engine
from routers import items

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Ecommerce API"}

from fastapi import FastAPI
from models import Base
from database import engine
from routers import items
from routers import users
from routers import cart

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)
app.include_router(cart.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Ecommerce API"}

from fastapi import FastAPI
from models import Base
from database import engine
from routers import items
from routers import users
from routers import cart
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend URL
    allow_methods=["*"],  # GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Content-Type, Authorization, etc.
)

app.include_router(items.router)
app.include_router(users.router)
app.include_router(cart.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Ecommerce API"}

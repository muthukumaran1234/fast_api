from fastapi import FastAPI
from settings.database import init_db
from user.routes import router

app = FastAPI()

# Initialize Tortoise ORM
init_db(app)

app.include_router(router)

@app.get("/")
async def home():
    return {"message": "Tortoise ORM is working with FastAPI!"}

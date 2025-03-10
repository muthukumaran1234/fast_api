from fastapi import FastAPI
from settings.database import init_db

app = FastAPI()

# Initialize Tortoise ORM
init_db(app)

@app.get("/")
async def home():
    return {"message": "Tortoise ORM is working with FastAPI!"}

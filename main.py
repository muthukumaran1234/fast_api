from fastapi import FastAPI
from apps.users.routes import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/api")

from fastapi import FastAPI
from apps.users.routes import router as user_router

app = FastAPI()
# including the router from the routes
app.include_router(user_router, prefix="/api")

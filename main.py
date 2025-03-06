from fastapi import FastAPI
from apps.users.routes import router as user_router
from apps.image_upload import image
from apps.aws_s3 import aws_image
app = FastAPI()
# including the router from the routes
app.include_router(user_router, prefix="/api")
app.include_router(image ,prefix="/image")
app.include_router(aws_image ,prefix="/aws_images")

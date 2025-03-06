import json

with open("././env.json") as f:
    config = json.load(f)

AWS_REGION= config["AWS_REGION"]
AWS_SNS_ARN= config["AWS_SNS_ARN"] 
AWS_ACCESS_KEY= config["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS= config["AWS_SECRET_ACCESS"]
AWS_STORAGE_BUCKET_NAME= config["AWS_STORAGE_BUCKET_NAME"]
AWS_STORAGE_FOLDER_NAME= config["AWS_STORAGE_FOLDER_NAME"]


import boto3
from botocore.exceptions import NoCredentialsError
import uuid
from sqlalchemy.orm import Session
from fastapi import FastAPI, File, UploadFile, Depends,APIRouter, HTTPException
from sqlalchemy.orm.attributes import flag_modified

from apps.users.models import User
from core.database import get_db

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS,
    region_name=AWS_REGION
)

def upload_image_to_s3(file: UploadFile):
    try:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_key = f"{AWS_STORAGE_FOLDER_NAME}/{unique_filename}"

        # Upload file to S3
        s3_client.upload_fileobj(
            file.file,
            AWS_STORAGE_BUCKET_NAME,
            file_key,
            ExtraArgs={"ACL": "public-read", "ContentType": file.content_type}
        )

        # Generate public URL
        public_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"

        return public_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials are not valid")

aws_image = APIRouter()

@aws_image.post("/upload/{user_id}")
def upload_image(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    public_url = upload_image_to_s3(file)
    # Fetch User & Store Image URL in JSON field
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    if not user.image_urls:
        user.image_urls = []  # Initialize JSON field as list

    user.image_urls.append(public_url)  # Append new URL
    
    # Mark JSON field as modified
    flag_modified(user, "image_urls")
    
    db.commit()
    db.refresh(user)

    return {"message": "Image uploaded", "image_urls": user.image_urls}

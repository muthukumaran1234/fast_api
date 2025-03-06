from fastapi import FastAPI, File, UploadFile, Depends,APIRouter
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm import Session
from supabase import create_client
from apps.users.models import User
from core.database import get_db

image = APIRouter()

import json

with open("././env.json") as f:
    config = json.load(f)

# Supabase Config
SUPABASE_URL = config["SUPABASE_URL"]     
SUPABASE_KEY = config["SUPABASE_KEY"]  
SUPABASE_BUCKET = config[ "SUPABASE_BUCKET"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url("images/vigay.jpg")
print("Public URL:", public_url)


@image.post("/upload/{user_id}")
def upload_image(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_content = file.file.read()
    file_name = f"user_{user_id}/{file.filename}" 

    # Upload to Supabase
    response = supabase.storage.from_(SUPABASE_BUCKET).upload(file_name, file_content)
    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)

    # Fetch User & Store Image URL in JSON field
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # if not user.image_urls:
    #     user.image_urls = []  # Initialize JSON field as list
    print(user.image_urls)
    user.image_urls.append(public_url)  # Append new URL
    print(user.image_urls)
    
    # Mark JSON field as modified
    flag_modified(user, "image_urls")
    
    db.commit()
    db.refresh(user)

    return {"message": "Image uploaded", "image_urls": user.image_urls}

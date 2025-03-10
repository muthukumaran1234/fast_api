from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

DATABASE_URL = "postgres://postgres:n7SJK*H!!NFzsNt@db.okbzsjmrejnmhbhabdez.supabase.co:5432/postgres"

# FastAPI function to initialize database
def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["user.models"]},  # Where to find models
        generate_schemas=True,  # Auto-creates tables if they don’t exist (Only for development)
        add_exception_handlers=True,  # Handles database-related errors automatically
    )

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": ["user.models", "aerich.models"],  # Include aerich.models
            "default_connection": "default",
        }
    }
}

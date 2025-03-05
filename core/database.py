from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
DATABASE_URL = "postgresql+psycopg2://postgres.uicdyanzztdwumhxqzhl:cbemlad01jElgxxm@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# Create Sync Engine
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
# Create Sync Session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


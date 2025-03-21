from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace these values with your actual PostgreSQL credentials and database name.
DATABASE_URL = "postgresql://return_db_user:vGgEdkbrROKXPWACa04QqyOIYbvH8kRF@dpg-cvcgadbtq21c739unjr0-a.ohio-postgres.render.com/return_db"

# Create the SQLAlchemy engine.
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class.
SessionLocal = sessionmaker(bind=engine)

# Base class for our models.
Base = declarative_base()

# Dependency that will be used in FastAPI endpoints.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

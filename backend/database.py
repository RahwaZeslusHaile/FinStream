from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import os 
import shutil


IS_LAMBDA = "AWS_LAMBDA" in os.environ
if IS_LAMBDA: 
    db_path = "/tmp/FinStream.db"

    src_path = os.path.join(os.path.dirname(__file__), "FinStream.db")
    if not os.path.exists(db_path) and os.path.exists(src_path):
        shutil.copy2(src_path, db_path)
        
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///.FinStream.db"
        

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



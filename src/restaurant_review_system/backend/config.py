import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship,sessionmaker,declarative_base


load_dotenv()

DATABASE_URL=f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}"

engine=create_engine(DATABASE_URL,echo=False)
Base=declarative_base()
session=sessionmaker(bind=engine)


def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()
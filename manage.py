from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, DECIMAL, select, func
from sqlalchemy.orm import mapped_column, relationship
from db import db
from app import app
from models import Book

def create_tables():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        create_tables() # creates all tables in the database
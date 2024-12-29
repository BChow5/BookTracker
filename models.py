from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, DECIMAL, DateTime, select
from sqlalchemy.orm import mapped_column, relationship
from db import db

class Book(db.Model):
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    author = mapped_column(String)
    rating = mapped_column(Integer, default=0)
    status = mapped_column(String, default="Plan To Read")
    progress = mapped_column(Integer, default=0)
    total_pages = mapped_column(Integer)
    thumbnail = mapped_column(String)
    
    
    

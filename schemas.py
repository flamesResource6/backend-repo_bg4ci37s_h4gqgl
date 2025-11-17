"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Solace Counselling Schemas

class Inquiry(BaseModel):
    """
    Public contact inquiries submitted from the website.
    Collection name: "inquiry"
    """
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = Field(None, description="Contact phone number")
    subject: str = Field(..., min_length=3)
    message: str = Field(..., min_length=10)
    consent: bool = Field(True, description="User consent to be contacted")
    source: Literal['contact','footer','hero','booking','other'] = 'contact'
    submitted_at: Optional[datetime] = None

class Appointment(BaseModel):
    """
    Appointment requests from booking form.
    Collection name: "appointment"
    """
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    preferred_date: str = Field(..., description="Preferred date (YYYY-MM-DD)")
    preferred_time: str = Field(..., description="Preferred time (HH:MM)")
    service: Literal['Individual Therapy','Couples Therapy','Family Therapy','Child & Adolescent','Trauma Support','Anxiety & Depression']
    notes: Optional[str] = Field(None, max_length=2000)
    consent: bool = Field(True)
    submitted_at: Optional[datetime] = None

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!

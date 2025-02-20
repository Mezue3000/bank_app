# import dependencies
from __future__ import annotations
from sqlmodel import SQLModel, Relationship, Field
from typing import Optional, List
from datetime import datetime, date, timezone


# create customer model
class Customer(SQLModel, table=True):
    customer_id: Optional[int] = Field(default= None, primary_key= True)
    first_name: str = Field(max_length=50, nullable=False, index=True)
    middle_name: Optional[str] = Field(max_length=50)
    surname: str = Field(max_length=50, nullable=False)
    birth_date: date = Field(nullable=False)
    email: str = Field(max_length=50, unique=True, nullable=False)
    phone_no: str = Field(max_length=45, nullable=False, unique=True)
    address: str = Field(max_length=75, nullable=False)
    
    
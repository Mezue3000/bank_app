# import dependencies
from __future__ import annotations
from sqlmodel import SQLModel, Relationship, Field
from typing import Optional, List
from datetime import datetime, date, timezone
from enum import Enum
from sqlalchemy import CheckConstraint
from decimal import Decimal


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
    
    accounts: List[Account] = Relationship(back_populates="customer")


# validate account_type
class AccountType(str, Enum):
    savings = "savings"
    current = "current"
    fixed = "fixed"
    domicilary = "domicilary"
    salary = "salary"
    
    
# create account model
class Account(SQLModel, table=True):
    account_id: Optional[int] = Field(default=None, primary_key=True)
    account_type: AccountType = Field(nullable=False)
    account_number: str = Field(min_length=11, max_length=11, nullable=False)
    balance: Decimal = Field(default=Decimal("0.00"), sa_column_kwargs={"type": "Numeric(14, 2)"})
    customer_id: int = Field(
                        foreign_key="customer.customer_id", sa_column_kwargs={"onupdate": "CASCADE", "ondelete": "NO ACTION"})
    
    customer:Customer = Relationship(back_populates="accounts")
     
    __table_args__ = (
        CheckConstraint("account_type IN('savings', 'current', 'fixed', 'domicilary', 'salary')", name= "valid_account_types"))
    
    
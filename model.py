# import dependencies
from __future__ import annotations
from sqlmodel import SQLModel, Relationship, Field, CheckConstraint, func
from typing import Optional, List
from datetime import datetime, date, timezone
from enum import Enum
from decimal import Decimal


# create customer model
class Customer(SQLModel, table=True): 
    customer_id: Optional[int] = Field(default= None, primary_key= True)
    first_name: str = Field(..., max_length=50, index=True)
    middle_name: Optional[str] = Field(max_length=50)
    surname: str = Field(..., max_length=50)
    birth_date: date = Field(...)
    email: str = Field(..., max_length=50, unique=True)
    phone_number: str = Field(..., max_length=45, unique=True)
    address: str = Field(..., max_length=75)
    
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
    account_type: AccountType = Field(...)
    account_number: str = Field(..., min_length=10, max_length=10)
    balance: Decimal = Field(default=Decimal("0.00"), sa_column_kwargs={"type": "Numeric(14, 2)"})
    customer_id: int = Field(
        foreign_key="customer.customer_id", sa_column_kwargs={"onupdate": "CASCADE", "ondelete": "NO ACTION"})
    
    customer:Customer = Relationship(back_populates="accounts" )
    transactions:List[Transaction] = Relationship(back_populates="account") 
     
    __table_args__ = (
        CheckConstraint("account_type IN('savings', 'current', 'fixed', 'domicilary', 'salary')", name= "valid_account_types"))


# validate transaction type
class TransactionType(str, Enum):
    deposite = "deposite"
    withdrawal = "withdrwal"
    transfer = "transfer"
    payment = "payment"
    credit = "credit"
    foreign = "foreign"


# create Transaction model
class Transaction(SQLModel, table=True):
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    transaction_type: TransactionType = Field(...)
    transaction_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False) 
    transaction_amount: Decimal = Field(..., gt=0, sa_column_kwargs={"type": "Numeric(14,2)"})
    transaction_reference: str = Field(max_length=50, nullable=False)
    transaction_status: str = Field(max_length=50, nullable=False) 
    account_id: int = Field(
        foreign_key="account.account_id",
        sa_column_kwargs={"onupdate": "CASCADE", "ondelete": "NO ACTION"})
     
    account:Account = Relationship(back_populates="transactions")
    transfer_sender: Optional[Transfer] = Relationship(
        back_populates="sender_transaction", 
        sa_relationship_kwargs={"uselist": False})
    
    transfer_receiver: Optional[Transfer] = Relationship(
        back_populates="receiver_transaction", 
        sa_relationship_kwargs={"uselist": "receiver_transaction"})
    
    __table_arg__ = (CheckConstraint("transaction_type IN('deposit', 'withdrawal', 'transfer', 'payment', 'credit', 'foreign')", name="valid_transaction_type")) 
    
    __table_arg__ = (CheckConstraint("transaction_amount > 0", name= "transaction_amount_positive"))   


# create tranfer model
class Transfer(SQLModel, table=True):
    transfer_id: Optional[int] = Field(default=None, primary_key=True)
    transfer_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    amount: Decimal = Field(..., gt=0.00, sa_column_kwargs={"type": "Numeric(14, 2)"})
    sender_name: Optional[str] = Field(max_length=50)
    beneficiary_name: Optional[str] = Field(max_length=50)
    sender_transaction_id: Optional[int] = Field(foreign_key=True, unique=True)
    receiver_transaction_id: Optional[int] = Field(foreign_key=True, unique=True)
    
    sender_transaction: Transaction = Relationship(back_populates="transfer_sender")
    receiver_transaction: Transaction = Relationship(back_populates="transfer_receiver")
    
    __table_arg__ = (CheckConstraint("amount > 0", name= "transfer_amount_positive")) 
    

# create card model  
 

    
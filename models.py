from sqlalchemy import String,Numeric,Date
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime
from db import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    vendor: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Numeric,nullable=False)
    date: Mapped[datetime] = mapped_column(Date,nullable=False)








    


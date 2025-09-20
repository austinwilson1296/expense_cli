import typer
from typing_extensions import Annotated
from datetime import datetime
from models import Transaction
from db import engine,SessionaLocal,Base
from sqlalchemy import select,delete
import logging
from rich import print
from rich.markup import escape
import csv
import pandas as pd

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def init_db():
    Base.metadata.create_all(engine)
    

app = typer.Typer() 



@app.command()
def add_transaction(
    vendor: str, 
    amount: float,
    date: Annotated[str, typer.Argument()] = datetime.strftime(datetime.now(),"%m/%d/%Y")
    ):
    with SessionaLocal() as session:
        new_date = datetime.strptime(date,"%m/%d/%Y")
        new_trans = Transaction(
            vendor = vendor,
            amount = amount,
            date = new_date
        )
        session.add(new_trans)
        session.commit()
    print("-----------------------")
    print(f"[bold green]Transaction Added: {vendor}[/bold green] 🎉")
    print("\n-----------------------")

@app.command()
def list_transactions():
    stmt = select(Transaction)
    with SessionaLocal() as session:
        for trans in session.scalars(stmt):
            print(f"ID: {trans.id}\n")
            print(f"Vendor: {trans.vendor}\n")
            print(f"Amount: {trans.amount:,.2f}\n")
            print(f"Date: {trans.date}\n")
            print("-----------------------\n")

@app.command()
def delete_transactions(id: int):
    stmt = delete(Transaction).where(Transaction.id==id)
    with SessionaLocal() as session:
        session.execute(stmt)
        session.commit()
    print(f"Succesfully Removed Transaction with id {id}")

@app.command()
def export_to_csv():
    stmt = select(Transaction)
    data_obj = []
    with SessionaLocal() as session:
        for trans in session.scalars(stmt):
            new_trans = {
                "id":trans.id,
                "vendor":trans.vendor,
                "amount":trans.amount,
                "date":trans.date
            }
            data_obj.append(new_trans)
    df = pd.DataFrame(data_obj)
    df.to_csv("transactions.csv")
        
        
    

if __name__=="__main__":
    init_db()
    app()
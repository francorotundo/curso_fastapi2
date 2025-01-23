from fastapi import FastAPI
from models import Transaction, Invoice
from db import create_all_tables
from .routers import customers, transactions, invoices, plans
import datetime    

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)

app.version = '1.0.0'

@app.get("/")
async def root():
    return {"message": f"Hola, Franco la hora es {datetime.datetime.now().strftime('%H:%M:%S')}"}


@app.get("/time/{n}")
async def time(n: int):
    return {"time": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {n}"}

from fastapi import status, HTTPException, APIRouter
from models import Invoice
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post("/invoices", tags=['Invoices'])
async def create_invoice(invoice_data: Invoice):
    return invoice_data
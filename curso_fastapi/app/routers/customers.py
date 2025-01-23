from fastapi import status, HTTPException, APIRouter
from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers']) ## Con response_model estamos definiendo el modelo con el que vamos a responder
async def create_customer(customer_data: CustomerCreate, session: SessionDep): ## Aquí estamos definiendo el modelo que vamos a recibir
    customer = Customer.model_validate(customer_data.model_dump())
    ## model_dump() muestra la información ingresada al post a traves de en este caso customer_data
    ## model_validate verifica la información ingresada con respecto al model Customer, y creando diche instancia
    session.add(customer)
    # la sentecia anterior estructura la información para que pueda ser guardada en la db
    session.commit()
    # el commit hace el se guarde la información en la base de datos
    session.refresh(customer)
    # el refresh actualiza la información de custormer con la información guardada en la base de datos
    # para que aparezca la información de customer.id que se agrega al guardarse en la db
    return customer


@router.get("/customers", response_model=list[Customer], tags=['Customers'])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all() 
    ### con la sentencia .where() dentro de exec despues de select
    # se puede realizar un filtro de la información extraida colocando dentro del parentesis 
    # el argumeno por ejemplo .where(and_(Customer.description == 'Developer', Customer.email == 'francorotundo90@gmail.com'))

@router.get("/customers/{customer_id}", response_model=Customer, tags=['Customers'])
async def read_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer: ## es igual que customer == None
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    return customer

@router.delete("/customers/{customer_id}", tags=['Customers'])
async def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer: ## es igual que customer == None
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"detail": "OK"}

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers'])
async def update_customer(customer_id: int, customer_data: CustomerUpdate,session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer: ## es igual que customer == None
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_data_update = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_data_update)
    session.add(customer)
    session.commit() 
    session.refresh(customer)
    return customer
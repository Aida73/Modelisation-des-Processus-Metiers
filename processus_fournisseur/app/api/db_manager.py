from fastapi import HTTPException
from .models import *
from .db import *
from sqlalchemy import insert,select, update, func




async def add_order(payload: Order):
    order_dict = payload.dict()
    if isinstance(order_dict['order_date'], datetime):
        order_dict['order_date'] = order_dict['order_date'].isoformat()
    
    if order_dict['service_delivery_date'] is not None and isinstance(order_dict['service_delivery_date'], datetime):
        order_dict['service_delivery_date'] = order_dict['service_delivery_date'].isoformat()

    if isinstance(order_dict['order_date'], str):
        order_dict['order_date'] = datetime.fromisoformat(order_dict['order_date'])
    
    if isinstance(order_dict['service_delivery_date'], str):
        order_dict['service_delivery_date'] = datetime.fromisoformat(order_dict['service_delivery_date'])
    # if isinstance(order_dict['order_date'], datetime):
    #     order_dict['order_date'] = order_dict['order_date'].isoformat()
    # if order_dict['service_delivery_date'] is not None and isinstance(order_dict['service_delivery_date'], datetime):
    #     order_dict['service_delivery_date'] = order_dict['service_delivery_date'].isoformat()

    query = orders.insert().values(**order_dict)
    print("query",query)
    return await database.execute(query=query)


async def get_order_by_id(order_id: str):
    query = select(orders).where(orders.c.order_id == order_id)
    return await database.fetch_one(query=query)

async def get_all_orders():
    query = select(orders)
    return await database.fetch_all(query=query)


async def add_client(payload: Client):
    client = {"client_id": payload.client_id, "username": payload.username}
    query = insert(clients).values(**client)
    return await database.execute(query=query)


async def get_all_clients():
    query = select(clients)
    return await database.fetch_all(query=query)


async def get_client_by_id(id_client: str):
    query = select(clients).where(clients.c.client_id == id_client)
    return await database.fetch_one(query=query)


async def update_order(order_id: str, update_values: dict):
    if 'service_delivery_date' in update_values and isinstance(update_values['service_delivery_date'], datetime):
        update_values['service_delivery_date'] = update_values['service_delivery_date'].isoformat()
    query = (
        update(orders)
        .where(orders.c.order_id == order_id)
        .values(**update_values)
    )
    await database.execute(query)
    return {"message": "Order updated successfully"}


async def get_orders_by_client(client_id: str):
    query = select(orders).where(orders.c.client_id == client_id)
    return await database.fetch_all(query=query)

async def add_devis(payload: Devis):
    query = devis.insert().values(**payload.dict())
    return await database.execute(query=query)

async def get_all_devis():
    query = select(devis)
    return await database.fetch_all(query=query)

async def update_devis(devis_id: str, status:str):
    query = devis.update().where(devis.c.devis_id == devis_id).values(status=status)
    return await database.execute(query=query)

async def add_realisation(payload: Realisation):
    query = insert(realisations).values(**payload.dict())
    return await database.execute(query=query)

async def get_pending_devis():
    query = select(devis).where(devis.c.status == "pending")
    return await database.fetch_all(query=query) 

async def get_confirmed_devis():
    query = select(devis).where(devis.c.status == "valide")
    return await database.fetch_all(query=query) 

async def get_orders_pending():
    query = select(orders).where(orders.c.status == "pending")
    return await database.fetch_all(query=query) 

async def get_orders_confirmed():
    query = select(orders).where(orders.c.status == "realise")
    return await database.fetch_all(query=query) 

async def get_orders_realized():
    query = select(orders).where(orders.c.status == "valide")
    return await database.fetch_all(query=query) 
async def get_all_realisations():
    query = select(realisations)
    return await database.fetch_all(query=query)

async def update_realisation(realisation_id: str, update_values: dict):
    query = (
        update(realisations)
        .where(realisations.c.realisation_id == realisation_id)
        .values(**update_values)
    )
    await database.execute(query)
    return {"message": "Realisation updated successfully"}

from fastapi import APIRouter, BackgroundTasks, HTTPException
from .models import *
import requests
from .db_manager import *
from app.client_tasks import app_cli
import httpx
from .rabbit import RabbitMQReceiver

router = APIRouter()

async def save_order(payload):
    return await add_order(payload)


async def save_client(payload):
    return await add_client(payload)


async def save_devis(payload):
    return await add_devis(payload)

async def save_realisation(payload):
    return await add_realisation(payload)

async def modify_devis(devis_id:str, status:str):
    return await update_devis(devis_id, status)

async def update_ex_order(order_id: str, update_values: dict):
    try:
        await update_order(order_id, update_values)
        print("Order updated successfully")
    except Exception as e:
        print(f"Failed to update order: {e}")
        
async def update_ex_realisation(realisation_id: str, update_values: dict):
    try:
        await update_realisation(realisation_id, update_values)
        print("Order updated successfully")
    except Exception as e:
        print(f"Failed to update realisation: {e}")

@router.post("/add_client")
async def new_client(payload: Client, background_tasks: BackgroundTasks):
    background_tasks.add_task(save_client, payload)
    response = {
        'message': f"Client successfully added!"
        }
    return response


@router.get("/clients")
async def get_clients():
    clients = await get_all_clients()
    return clients


@router.get("/orders")
async def get_orders():
    orders = await get_all_orders()
    return orders


@router.post("/devis")
async def post_devis(payload:Devis, background_tasks: BackgroundTasks):
    background_tasks.add_task(save_devis, payload)
    response = requests.post("http://processus_fournisseur:8000/devis", json=payload.dict())
    print(response.text)
    response = {
        "message": "Devis added successfully"
    }
    return response


# add new order
@router.post("/place_order")
async def new_order(payload: Order, background_tasks: BackgroundTasks):
    background_tasks.add_task(save_order, payload)
    response = {
        'message': "ok",
    }
    return response


@router.get("/devis")
async def get_devis():
    devis = await get_all_devis()
    return devis

@router.get("/devis/clients/{client_id}")
async def get_client_devis(client_id: str):
    devis = await get_devis_by_client_id(client_id)
    return devis


@router.get("/devis/{devis_id}")
async def get_devis(devis_id: str):
    devis = await get_devis_by_id(devis_id)
    return devis


@router.put("/devis")
async def put_devis(devis_id:str, status:str, backgroundtasks: BackgroundTasks):
    backgroundtasks.add_task(modify_devis,devis_id,status)
    if status=="valide":
        app_cli.send_task("client_tasks.validate_devis",args=[devis_id])
    response = {
        "message": "Status updated successfully"
    }
    return response
    
@router.put("/orders/{order_id}")
async def update_existing_order(background_tasks: BackgroundTasks, order_id: str, payload: OrderUpdate):
    update_values = payload.dict(exclude_unset=True)
    background_tasks.add_task(update_ex_order, order_id, update_values)
    # if update_values.status=="valide":
    #     app_prov.send_task("client_tasks.validate_order",args=[order_id])
    return {"message": "Order update initiated"}

@router.post("/add_realisation")
async def new_client(payload: Realisation, background_tasks: BackgroundTasks):
    background_tasks.add_task(save_realisation, payload)
    #id_client = await add_client(payload)
    response = {
        'message': f"Realisation successfully added!"
        }
    return response

@router.get("/realisations")
async def get_realisation():
    realisations = await get_all_realisations()
    return realisations


@router.put("/realisations/{realisation_id}")
async def update_existing_realisation(background_tasks: BackgroundTasks, realisation_id: str, payload: RealisationUpdate):
    update_values = payload.dict(exclude_unset=True)
    background_tasks.add_task(update_ex_realisation, realisation_id, update_values)
    app_cli.send_task("client_tasks.update_realisation",args=[realisation_id, update_values])
    return {"message": "Realisation update initiated"}
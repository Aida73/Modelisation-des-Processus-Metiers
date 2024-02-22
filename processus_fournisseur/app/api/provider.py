from fastapi import APIRouter, BackgroundTasks, HTTPException
from .models import Order
from .db_manager import *
import httpx

router = APIRouter()


async def save_order(payload):
    return await add_order(payload)


def check_order(order_id: int, background_tasks: BackgroundTasks):
    status = "valide"
    # ..../1
    verif_status = {'order_id':order_id, status:status}
    background_tasks.add_task(confirm_order, verif_status)


def confirm_order(verif_status):
    with httpx.Client() as client:
        response = client.post("client-endponit", json=verif_status)
    print(response.text)


# add new order
@router.post("/place_order")
async def add_order(payload: Order, background_tasks: BackgroundTasks):
    background_tasks.add_tasks(save_order, payload)
    response = {
        'message': f"Votre commande numero a été bien reçue et est en cours de traitement",
    }
    return response



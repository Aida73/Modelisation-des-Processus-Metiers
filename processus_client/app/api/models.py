from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


# class Provider(BaseModel):
#     provider_id: str
#     username: str

class Client(BaseModel):
    client_id: str
    username:  str

class Order(BaseModel):
    order_id: str
    service: str
    status: str
    order_date: Optional[datetime] = Field(default_factory=datetime.now)
    service_delivery_date: Optional[datetime] = None
    client_id: str


class Devis(BaseModel):
    devis_id: str
    order_id: str
    status: str
    devis_date: str
    devis_delivery_date: str

class ExistingDevis(BaseModel):
    devis_id: str
    status: str
    devis_date: str
    devis_delivery_date: str
    order: Order

    class Config:
        orm_mode = True


class Realisation(BaseModel):
    realisation_id: str
    order_id: str
    description: str
    realisation_date: str
    
class OrderUpdate(BaseModel):
    status: str
    service_delivery_date: Optional[datetime] = Field(default_factory=datetime.now)

class RealisationUpdate(BaseModel):
    description: str


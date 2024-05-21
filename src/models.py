from pydantic import BaseModel


class Order(BaseModel):
    stocks: str
    quantity: float
    status: str
    id: int

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from routers import UserRouter

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None]


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(UserRouter.router)

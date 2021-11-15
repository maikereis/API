from typing import Optional

from fastapi import Body, Form, FastAPI
from pydantic import BaseModel

from models import CashBackTransaction
app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.post("/items/{item_id}")
async def update_item(transaction : CashBackTransaction = Body(None)):
    results = {"transaction": transaction}
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_body:app", host="127.0.0.1", reload=True, port=8000)

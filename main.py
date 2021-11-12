from models import CashBack
from fastapi import FastAPI


app = FastAPI()

@app.get("/")

def read_root():
    return {"CashBack API": "Hello World!"}


@app.put("/api/cashback/{cashback_id}")
async def request_cashback(cashback_id: int, cashback: CashBack):
    """
        This function receives a PUT request
    """
    results = {"cashback_id": cashback_id, "sold_at": cashback.sold_at}
    return results
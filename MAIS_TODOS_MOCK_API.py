from datetime import datetime, timezone
from fastapi import Depends, FastAPI


from models import Record, CashBackRecord

app = FastAPI()


@app.get("/")
def read_root():
    return {"MAIS TODOS": "Hello World!"}


@app.post("/Cashback/")
async def create_cashback(record: Record):

    created_at_now = datetime.now(timezone.utc)

    response = CashBackRecord(
        created_at=created_at_now,
        message="successfully created cashback!",
        id="",
        record = record
    )
    return response



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("MAIS_TODOS_MOCK_API:app", host="127.0.0.1", reload=True, port=8001)
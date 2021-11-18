import requests
from fastapi import Body
from logs.customlogger import logger
from models import CashBackTransaction, Record, CashBackRecord
from db_api.info_tb import PRODUCT_CASHBACK

MAIS_TODOS_MOCK_API_URL = "http://127.0.0.1:8001/Cashback/"


# Search in a database table the cashback rate of product
def get_cashback_rate(category, database=PRODUCT_CASHBACK):
    return database[category]


def create_record(transaction: CashBackTransaction = Body(None)):
    logger.info("called")

    cashback_total = 0

    for p in transaction.products:
        cashback_total += get_cashback_rate(p.category) * p.value * p.quantity

    new_record = Record(
        cpf=transaction.customer.cpf, cashback=cashback_total
    )

    return new_record


def create_cashback(record: Record):

    mais_todos_response = requests.post(
        MAIS_TODOS_MOCK_API_URL,
        headers={"Content-Type": "application/json"},
        json={"cpf": record.cpf, "cashback": record.cashback},
    )

    if mais_todos_response.status_code != 200:
        return {"status": "error, your cashback can't be created!"}

    try:
        cashback_record = CashBackRecord(**mais_todos_response.json())
        return cashback_record
    except Exception as e:
        logger.error(e)
        return {"status": "error, your cashback can't be created!"}

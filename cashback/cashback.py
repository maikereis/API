import requests
from requests.structures import CaseInsensitiveDict

from fastapi import Body
from logs.customlogger import logger
from models import CashBackTransaction, Document
from db_api.info_tb import PRODUCT_CASHBACK

MAIS_TODOS_API_URL = "https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback"

# Search in a database table the cashback rate of product
def get_cashback_rate(category, database=PRODUCT_CASHBACK):
    return database[category]


def calculate_cashback(transaction: CashBackTransaction = Body(None)):
    logger.info("called")
    total_refound = 0

    for p in transaction.products:
        total_refound += get_cashback_rate(p.category) * p.value * p.quantity

    return total_refound


def send_to_mais_TODOS(document: Document):
      
    response = requests.post(
        MAIS_TODOS_API_URL,
        headers={"Content-Type":"application/json"},
        data={"document": document.doc_id, "cashback": document.cashback},
    )

    """ 
    THE END

    TEST IF THE RESPONSE FORMAT IS A DocumentResponse object 
    
    
    if response == DocumentResponse():
        doc_resp = DocumentResponse(response)
        return doc_resp
    else:
        return None
    """
    return False
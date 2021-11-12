from typing import List
from pydantic import BaseModel


class Customer(BaseModel):
    """
    In cashback transactions we have a client, this class define a customer

    Attributes
    ----------

    customer_name : str
        a string containing the customer name

    customer_cpf : int
        a 11-digit number that represents a Brazilian identification document
    """

    customer_name: str
    customer_cpf: int

class Product(BaseModel):
    """
    In cashback transactions we have products, this class define a product

    Attributes
    ----------

    product_type : str
        the type of a product: 'A', 'B' or 'C'

    value : float
        the price of the product

    quantity: int
        the quantity of the product
    """

    product_type: str
    value: float
    quantity: int

class CashBackTransaction(BaseModel):
    """
    In cashback transactions we have a transaction datetime, customer, and product or products.
    This class define a CashBack transaction.

    Attributes
    ----------

    sold_at : str
        the datetime of a transaction in a format 'yyyy-mm-dd HH:MM:ss'

    customer : Customer
        the customer responsible for the transaction
    
    products: List[Product]
        a list of products in the transaction
    """
    sold_at: str
    customer: Customer
    products: List[Product]
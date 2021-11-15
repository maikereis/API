from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta


class Customer(BaseModel):
    """
    Description

        In cashback transactions we have a client, this class define
        a customer.

    Attributes:
        customer_name : str

            a string containing the customer name.

        customer_cpf : int

            a 11-digit number that represents a Brazilian identification
            document.
    """

    customer_name: str
    customer_cpf: int


class Product(BaseModel):
    """
    Description

        In cashback transactions we have products, this class define a product.

    Attributes

        product_type : str

            the type of a product: 'A', 'B' or 'C'.

        value : float

            the price of the product.

        quantity: int

            the quantity of the product.
    """

    product_type: str
    value: float
    quantity: int


class CashBackTransaction(BaseModel):
    """
    Description

        In cashback transactions we have a transaction datetime, customer,
        and product or products. This class define a CashBack transaction.

    Attributes

        sold_at : str

            the datetime of the sale in a format
            'yyyy-mm-dd HH:MM:ss'.

        customer : Customer

            the customer responsible for the transaction.

        products: List[Product]

            a list of products in the transaction.
    """
    sold_at: datetime
    customer: Customer
    total: float
    products: List[Product] = []


class User(BaseModel):
    """
    Description

        The class that represents an API user/client.

    Attributes

        username : str

            the client username.

        full_name : str

            the client full name.

        email : str

            the client e-mail.

        disabled: bool

            if the client is enabled or not.

    """
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    """
    Description

        The class that represents an API user/client in DB.

    Attributes

        User: user

            the user information.

        hashed_password : str

            the hashed password of the user stored on the database.
    """
    hashed_password: str


class Token(BaseModel):
    """
    Description

        The class that represents the response when a client request an
        authorization token.

    Attributes

        access_token : str

            the JWT token generated using the client information and
            an expiration date.

        token_type : str

            the token type.
    """
    access_token: str
    token_type: str


class TokenOwner(BaseModel):
    """
    Description

        The class that represents the response when a client request an
        authorization token.

    Attributes

        username : str

            the token owner.
    """
    username: Optional[str] = None


class JWTPayload(BaseModel):
    """
    Description

        The class that represents the JSON Web Token payload.

    Attributes

        sub : str

            the subject.

    Methods

        update_exp_date

    """
    sub: str
    exp: Optional[datetime]

    def update_exp_date(self, lifetime: timedelta = timedelta(minutes=15)):
        """
        Update the expiration date by adding the lifetime to the currente
        datetime.

        Paramns:

            lifetime : timedelta

        """
        self.exp = self.datetime.utcnow() + lifetime

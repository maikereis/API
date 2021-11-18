import re
import numpy as np
from datetime import datetime, timedelta, timezone

from logs.customlogger import logger
from typing import List, Optional
from pydantic import BaseModel, validator
from db_api.info_tb import PRODUCT_CATEGORIES


RE_NAMES = "[A-Za-z]{2,30}"
RE_FULLNAMES = "^[a-zA-Z]{2,40}(?: [a-zA-Z]+){0,4}$"
RE_EMAILS = "^[a-z0-9.]+@[a-z0-9]+.([a-z]+).([a-z]+)"
# A date in the past
VERY_OLD = datetime(2000, 1, 1, 0, 0)
# Transaction delay equivalent to timedelta(milliseconds=1)
DELAY = 0.001


class Customer(BaseModel):
    """
    Description

        In cashback transactions we have a client, this class define
        a customer.

    Attributes:
        name : str

            a string containing the customer name.

        cpf : int

            a 11-digit number that represents a Brazilian identification
            document.
    """

    name: str
    cpf: str

    @validator('name')
    def name_validator(cls, name):
        if re.fullmatch(RE_NAMES, name) is None:
            raise ValueError("product name invalid")
        return name

    def validate_cpf(cpf_to_validate: str):
        try:
            # Convert the string to a list of integers
            cpf_as_list = list(map(int, cpf_to_validate))
            # Remove last two digits
            cpf = cpf_as_list[:-2]

            # Create arrays to perfom the validation
            validator_arr_digit1 = np.arange(2, 11)[::-1]
            validator_arr_digit2 = np.arange(2, 12)[::-1]

            # Calculate the first validator digit
            acc = np.dot(cpf, validator_arr_digit1)
            first_digit = 11 - (acc % 11)
            if first_digit > 9:
                first_digit = 0

            # Insert digit on the cpf
            cpf.append(first_digit)

            # Calculate the last validator digit
            acc = np.dot(cpf, validator_arr_digit2)
            second_digit = 11 - (acc % 11)
            second_digit

            # Insert digit on the cpf
            cpf.append(second_digit)

            # Verify if the numbers matches
            return cpf == cpf_as_list
        except ValueError as e:
            logger.error(e)
        return False

    @validator('cpf')
    def cpf_validator(cls, cpf):
        if not cls.validate_cpf(cpf):
            logger.error('invalid cpf')
            raise ValueError('invalid cpf')
        return cpf


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

    # Keep these ordering because @validador 'values' param
    # returns the values of the variables declared above
    category: str
    quantity: int
    value: int

    @validator('category')
    def category_has_only_letters(cls, category):
        # Check if the product name has only letters (ignoring cap),
        if re.fullmatch(RE_NAMES, category) is None:
            logger.error('invalid product name')
            raise ValueError('invalid product name')
        return category

    @validator('category')
    def category_is_in_db(cls, category):
        if category not in PRODUCT_CATEGORIES:
            logger.error('unknown product')
            raise ValueError('unknown product')
        return category

    @validator('quantity')
    def quantity_is_positive(cls, quantity):
        if quantity < 0:
            logger.error('negative quantity')
            raise ValueError('negative quantity')
        return quantity

    @validator('value')
    def value_is_positive(cls, value):
        if value < 0:
            logger.error('negative value')
            raise ValueError('negative value')
        return value

    # 'values' will return the params 'category', and 'quantity'
    @validator('value')
    def has_value_must_have_quantity(cls, value, values):
        try:
            if value != 0 and values['quantity'] == 0:
                logger.error('whitout quantity')
                raise ValueError("whitout quantity")
            return value
        except KeyError:
            logger.error('invalid quantity')
            raise ValueError("invalid quantity")


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
    # Keep these ordering because @validador 'values' param returns the values
    # of the variables declared above, so when we need the param 'products' to
    # evaluate the 'total' it will validated and available
    sold_at: datetime = datetime.now(timezone.utc)
    customer: Customer
    products: List[Product]
    total: float

    @validator('sold_at')
    def sold_at_is_a_valid_time(cls, sold_at):
        # Get the current time at UTC
        now = datetime.now(timezone.utc)
        # Check if the transaction datetime is too old or
        # was made in the future
        if (sold_at.timestamp() < VERY_OLD.timestamp()):
            logger.error('the sold_at is very old')
            raise ValueError('no way, at that time it was all bush')

        if ((sold_at.timestamp() + DELAY) > now.timestamp()):
            logger.error('the sold_at occurs in the future?')
            raise ValueError('who are you, the Marty McFly ?')
        return sold_at

    def sum_products_values(products: List[Product]):
        calculated_total = 0
        for p in products:
            calculated_total += p.value * p.quantity
        return calculated_total

    @validator('total')
    def total_of_products_match(cls, total, values):
        try:
            if total != cls.sum_products_values(values['products']):
                logger.error('the total of products differs')
                raise ValueError('the total of products differs')
            return total
        except KeyError:
            logger.error('invalid products')
            raise ValueError('invalid products')

class Record(BaseModel):
    cpf : str
    cashback : float

    @validator('cashback')
    def cashback_is_positive(cls, cashback):
        if cashback < 0:
            logger.error('negative cashback')
            raise ValueError('negative cashback')
        return cashback


class CashBackRecord(BaseModel):
    created_at : datetime
    message : str
    id : str
    record : Record


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

    # Verify if username has only letters
    @validator('username')
    def username_has_only_letters(cls, username):
        if re.fullmatch(RE_NAMES, username) is None:
            logger.error('invalid username')
            raise ValueError('invalid username')
        return username

    # Verifies if the full name has only letters and spaces (can have 5 names)
    @validator('full_name')
    def full_name_has_only_letters(cls, full_name):
        if re.fullmatch(RE_FULLNAMES, full_name) is None:
            logger.error('invalid full name')
            raise ValueError('invalid full name')
        return full_name

    # Verifies if the email matches the format "a.b.c@d.e.f"
    @validator('email')
    def email_has_correct_format(cls, email):
        if re.fullmatch(RE_EMAILS, email) is None:
            logger.error('invalid e-mail')
            raise ValueError('e-mail invalid')
        return email


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

    # Verify if username has only letters
    @validator('username')
    def username_has_only_letters(cls, username):
        if re.fullmatch(RE_NAMES, username) is None:
            raise ValueError("username name invalid")
        return username


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
        self.exp = self.datetime.now(timezone.utc) + lifetime

    # Verify if username has only letters
    @validator('sub')
    def subject_has_only_letters(cls, sub):
        if re.fullmatch(RE_NAMES, sub) is None:
            raise ValueError("username name invalid")
        return sub

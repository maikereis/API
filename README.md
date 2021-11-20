<h1> CashBackAPI </h1>

This is a cashback API made using fastapi. This API receives a request with a [cashback transaction](models.py), like:

    {
        "sold_at": "2021-11-20T12:59:39.190588+00:00",
        "customer": {"name": "Joao Rodrigues","cpf": "00000000000"},
        "products": [
            {"category": "books","quantity": 10,"value": 1}
            {"category": "clothes","quantity": 1,"value": 100},
        ],
        "total": 110
    }

after make all the validations, this API will request a cashback to [MAIS_TODOS_MOCK_API](MAIS_TODOS_MOCK_API.py), that will answer with a [cashback record](models.py), something like:

    {
        "created_at": "2021-11-20T12:59:39.500588+00:00",
        "message": "successfully created cashback!",
        "id": "32286cb0-4a07-11ec-bcf7-107b443a2030",
        "record": {"cpf": "00000000000","cashback": 0.4}
    }

<h2> Install Requirements </h2>

    'pip install -r requirements.txt'

<h2> Setting Environment variables </h2>

The [security](security) module is responsible for _encoding_, and _decoding_ the JWT. To perform these tasks, it needs a **secret key**, **algorithm**, and a token **lifetime**, all are sensitive information, in order to store these variables, it uses pydantic settings and .env files.

The [config](config.py) file defines a class **Authorization Settings**, that when it is instantiated it searches in the file .env (in the project root folder) for variables.

Create a file **.env** with:

    /.env:

    SECRET_KEY="4677b25090805fd888f642f9df5691ce7d9deef2e8a8af150ebdf765286fa87e"
    ALGORITHM="HS256"
    LIFETIME_MINUTES=30

Use the following command to generate the SECRET_KEY:

    > openssl rand -hex 32



<h2> Start </h2>

To start the [MOCK API](MAIS_TODOS_MOCK_API.py):

    > uvicorn MAIS_TODOS_MOCK_API:app2 --port 8001 --reload


To start the [CashBackAPI](main.py):


    > uvicorn main:app --reload

The [Swagger UI](https://swagger.io/tools/swagger-ui/) for the applications will be available on:

&emsp;&emsp;CashBackAPI - http://127.0.0.1:8001/docs 

&emsp;&emsp;MOCKAPI - http://127.0.0.1:8000/docs

<h2> Try Out </h2>

Open the SwaggerUI for the CashBackAPI, there are three available functions

    GET - Read Root
    POST - Request New Token
    POST - Validate Cashback Transaction

<h3> GET - Read Root </h3>

Will just return a message if the server if running

<h3> POST - Request New Token </h3>

Will return a new JWT for the API user. You must pass an username, and password the request the token, to test purposes use:

    username - johndoe
    password - secret

<h3>  POST - Validate Cashback Transaction </h3>

This is the core of the CashBackAPI, after receive a valid token, the user can send the cashback transaction to be validated, and the registred by the mais todos API.

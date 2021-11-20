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





from fastapi import Depends, Body, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from logs.customlogger import logger
from models import User, Token, TokenOwner
from exceptions import credentials_exception
from exceptions import non_user_exception, inactive_user_exception
from security.autorization import get_jwt, verify_jwt
from security.authentication import query_database, authenticate_user
from cashback.cashback import create_record, create_cashback

app = FastAPI()


@app.get("/")
def read_root():
    logger.info("called")
    return {"CashBack API": "Hello World!"}


@app.post("/token", response_model=Token)
async def request_new_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Try to get a client access token. The client must
    :func:`request_new_token` passing a
    [Form](https://fastapi.tiangolo.com/tutorial/request-forms/)
    data with a content-type 'x-www-urlencode' in the resquest.
    """
    logger.info("called")

    # Try to identify a client in the database
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise non_user_exception

    jwt = get_jwt(user.username)
    # Return the token to the client
    response_token = Token(access_token=jwt, token_type="bearer")

    return response_token.dict()


async def identify_user(token_owner: TokenOwner = Depends(verify_jwt)):
    logger.info("called")
    user = query_database(username=token_owner.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/api/cashback/")
async def validate_cashback_transaction(
    current_user: User = Depends(identify_user),
    record: str = Depends(create_record),
):
    logger.info("called")
    if current_user.disabled:
        logger.error("Inactive User / Access Denied")
        raise inactive_user_exception

    return create_cashback(record)
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8000)

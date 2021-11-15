from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from logs.api_logger import logger
from models import User, Token, TokenOwner
from exceptions import credentials_exception
from exceptions import non_user_exception, inactive_user_exception
from security.autorization import get_jwt, verify_jwt
from security.authentication import query_database, authenticate_user


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


async def get_current_active_user(current_user: User = Depends(identify_user)):
    logger.info("called")
    if current_user.disabled:
        raise inactive_user_exception
    return current_user


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Try to identify the user by the passed token as a header
    The function :func:`read_users_me` calls :func:`identify_user`
    (by [Depends()](https://fastapi.tiangolo.com/tutorial/dependencies/)
    stack) that receives a token as a parameter, then tries to decode
    the user,if the user was successfully decoded and the token is still
    valid, returns the user.

    """
    logger.info("called")
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user:
                         User = Depends(get_current_active_user)):
    logger.info("called")
    return [{"item_id": "Foo", "owner": current_user.username}]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8000)

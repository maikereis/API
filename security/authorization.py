from jose import JWTError, JWSError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from models import JWTPayload, TokenOwner
from config import AuthorizationSettings
from logs.customlogger import logger

from exceptions import (
    expired_signature_exception,
    internal_error_exception,
    credentials_exception,
)


auth_settings = AuthorizationSettings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt(sub: str):
    """
    Create the JWT by passing a :func:`sub` (subject) and a `exp`\
    (expiration). The `auth_settings` load the `secret_key`, \
    `algorithm` and `lifetime` from `.env` configuration file.

    Parameters:
        sub : str

            a JWT subject

    Returns:
        new_jwt : str

            a JWT string with {'sub':<subject>, 'exp':<datetime>}\
            encoded by secret_key, and algorithm.

    """
    logger.info("called")

    try:

        # Create the JSON Web Token
        jwt_payload = JWTPayload(
            sub=sub,
            exp=datetime.utcnow() + timedelta(minutes=auth_settings.lifetime),
        )

        # Encode the payload
        new_jwt = jwt.encode(
            jwt_payload.dict(),
            auth_settings.secret_key,
            algorithm=auth_settings.algorithm,
        )

        return new_jwt

    except JWSError:
        logger.error("JWT cannot be decode")
        raise internal_error_exception


async def verify_jwt(jwt_string: str = Depends(oauth2_scheme)):
    """
        When a :func:`jwt` token is passed, we need to:
         1. ensure that these token was signed by our API.
         2. is not expired.
         3. the token owner is a valid user in database.
        If successfully checked, returns the token \
        owner.

        Parameters:
            jwt: str

                A JWT passed by request.

        Returns:
            jwt_owner : TokenOwner

                The token owner identification.
    """
    logger.info("called")

    try:
        # Try to decode the JWT content.
        decoded_payload = jwt.decode(
            jwt_string,
            auth_settings.secret_key,
            algorithms=[auth_settings.algorithm],
        )
        # If successfully decoded, reads the content and access the
        # subject with, in this application, must contain the owner name.
        username: str = decoded_payload.get("sub")
        if username is None:
            logger.error("Invalid Credentials")
            raise credentials_exception

        jwt_owner = TokenOwner(username=username)
        return jwt_owner

    # Throw a Exception when the signature is expired
    except jwt.ExpiredSignatureError:
        logger.error("Token Signature Expired")
        raise expired_signature_exception
    # Throw a JWTError when the SECURITY_KEY, ALGORITHM, or anything
    # else goes wrong.
    except JWTError:
        logger.error("Invalid Credentials")
        raise credentials_exception

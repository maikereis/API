from jose import JWTError, JWSError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from models import JWTPayload, TokenOwner
from .settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_LIFETIME_MINUTES

from exceptions import (
    expired_signature_exception,
    internal_error_exception,
    credentials_exception,
)

from logs.customlogger import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt(jwt_payload: JWTPayload,
               secret=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM):
    """
        Create the JWT by passing a :func:`models.TokenPayload`.\
        It will use the in `settings.JWT_SECRET_KEY`, and \
        `settings.JWT_ALGORITHM` to encode the `jwt_payload`.

        Parameters:
            jwt_payload : JWTPayload

                a JWT payloab with 'sub'(subject) and 'exp'(expiration).

        Returns:
            encoded_jwt : str

                a JWT string.

    """
    logger.info("called")

    try:
        new_jwt = jwt.encode(jwt_payload.dict(), secret, algorithm=algorithm)
        return new_jwt
    except JWSError:
        logger.error('JWT cannot be decode')
        raise internal_error_exception


def get_jwt(sub, lifetime=JWT_LIFETIME_MINUTES):
    logger.info("called")
    # Create the JSON Web Token
    jwt_payload = JWTPayload(
        sub=sub, exp=datetime.utcnow() + timedelta(minutes=lifetime)
    )
    # Send payload ({'sub':string,'exp':datetime}) and receiber a JWT string
    jwt = create_jwt(jwt_payload)

    return jwt


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
            jwt_string, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        # If successfully decoded, reads the content and access the
        # subject with, in this application, must contain the owner name.
        username: str = decoded_payload.get("sub")
        if username is None:
            logger.error('Invalid Credentials')
            raise credentials_exception

        jwt_owner = TokenOwner(username=username)
        return jwt_owner

    # Throw a Exception when the signature is expired
    except jwt.ExpiredSignatureError:
        logger.error('Token Signature Expired')
        raise expired_signature_exception
    # Throw a JWTError when the SECURITY_KEY, ALGORITHM, or anything
    # else goes wrong.
    except JWTError:
        logger.error('Invalid Credentials')
        raise credentials_exception

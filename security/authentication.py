from passlib.context import CryptContext

from models import UserInDB
from db_api.fake_db import fake_users_db

from logs.customlogger import logger


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
        Verify if the passed password and the hashed_password found\
        in the database matches

        Parameters:
            plain_password : str

                a unhashed passord.

            hashed_password : str

                a hashed password.

        Returns:
            passwords_match : bool
    """
    logger.info("called")
    passwords_match = pwd_context.verify(plain_password, hashed_password)
    return passwords_match


def query_database(username: str, database=fake_users_db):
    """
        Function that search a :func:`user` in the database.

        Parameters:
            username : str

                the username of client, found in JWT payload send by request.

            database : List

                the database where the user's information is stored.

        Returns:
            user_info : UserInDB

                Returns the information found in the database about the user.
    """
    logger.info("called")
    # Simulate a database lookup.
    if username in database:
        user_dict = database[username]
        logger.success("a user found in database")
        user_info = UserInDB(**user_dict)
        return user_info


def authenticate_user(username: str, password: str, fake_db=fake_users_db):
    """
        Start the authentication process:
        1. Search the user in database.
        2. Verify if credentials (password) matches.

        Parameters:
            username : str
                the user identification, in this application an username.

            password : str
                the user password.

            fake_db : List, default 'fake_users_db'
                some database with user's information

    """
    logger.info("called")
    # Checking if the username matches any one name in the database.
    user = query_database(username, fake_db)
    if not user:
        return False
    # Some users can have the same name registered but not the same password.
    if not verify_password(password, user.hashed_password):
        return False
    logger.success("the user password matches")
    return user

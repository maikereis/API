from fastapi import HTTPException,  status
inactive_user_exception = HTTPException(status_code=400,
                                        detail="Inactive user")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
non_user_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
expired_signature_exception = HTTPException(
    status_code=403,
    detail="Expired signature",
    headers={"WWW-Authenticate": "Bearer"},
)
internal_error_exception = HTTPException(
    status_code=500,
    detail="For some obscure reason, when cannot generate your token"
)

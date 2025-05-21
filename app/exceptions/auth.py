from fastapi import HTTPException, status

incorrect_username_or_password_exp = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


unverified_credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


invalid_token_type_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token type",
    headers={"WWW-Authenticate": "Bearer"},
)


expired_token_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)

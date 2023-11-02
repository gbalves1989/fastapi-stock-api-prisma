from fastapi import status, HTTPException


def exception_error(message: str, status: int) -> HTTPException:
    return HTTPException(
        detail=message,
        status_code=status
    )


def exception_error_credential() -> HTTPException:
    return HTTPException(
        detail="Token invalid or expired",
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"}
    )

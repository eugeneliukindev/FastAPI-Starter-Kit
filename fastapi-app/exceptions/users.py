from fastapi.exceptions import HTTPException


def raise_user_already_exists_exp() -> HTTPException:
    raise HTTPException(status_code=409, detail="User already exists!")


def raise_user_not_found_exp() -> HTTPException:
    raise HTTPException(status_code=404, detail="User not found!")

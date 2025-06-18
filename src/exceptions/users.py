from fastapi import HTTPException, status


def raise_user_already_exists_exp() -> HTTPException:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists!")


def raise_user_not_found_exp() -> HTTPException:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

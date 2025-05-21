from fastapi import HTTPException, status

user_already_exists_exp = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User already exists!"
)


user_not_found_exp = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
)

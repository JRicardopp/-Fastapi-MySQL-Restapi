from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Path

from config.db import conn
from models.user import users
from schemas.user import User


from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get(
        path="/users", 
        response_model= User, 
        status_code=status.HTTP_200_OK, 
        summary = "show all Users", 
        tags=["Users"] 
        )
def get_users():
    """ Get Users

    Returns:
        json: List/Dict with the information of all users
    """
    return conn.execute(users.select()).fetchall()

@user.post(
        path="/",
        status_code=status.HTTP_201_CREATED,
        response_model= User,
        summary="Create a new User",
        tags=["Users"]
        )
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    print(result)
    return'created'


@user.put(
        path="/user/{id}/update",
        status_code=status.HTTP_201_CREATED,
        response_model=User,
        description=" Update a User by Id",
        tags=["Users"]
        )
def update_user(user: User, id: int):
    conn.execute(users.update().values(name=user.name, email=user.email, password= user.password).where(users.c.id == id))
    return conn.execute(users.select().where(user.c.id == id)).firts()



@user.delete(
            path="/users/{id}/delete",
            response_model=User, 
            
            tags=["Users"],
            summary="Delete a User"
            )
def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    return "Delete"
    




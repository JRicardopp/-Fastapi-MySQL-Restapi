from uuid import UUID
from cryptography.fernet import Fernet

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Path, Body, Form

from config.db import conn
from models.user import users
from schemas.user import User


key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()
#Show all Users#
@user.get(
        path="/users", 
        response_model= User, 
        status_code=status.HTTP_200_OK, 
        summary = "show all Users", 
        tags=["Users"] 
        )
def get_users():
    """Get Users
    This Path operations show all user in tha app

    Returns:
        200 (Ok) if get the list of users correctly 
    """
    return conn.execute(users.select()).fetchall()

#Show a User#
@user.get(
    path="/user",
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def get_a_user(id: str = Path(...)):
    """Get a User

    This path operations show a user in the app by id
    
    Args:
        id (str, optional): user id. Defaults to Path(...).

    Returns:
        200 (ok): if user id is correctly
    """
    return conn.execute(users.select().where(user.c.id == id)).first()

#Register a User#
@user.post(
        path="/",
        status_code=status.HTTP_201_CREATED,
        #response_model= User,
        summary="Create a new User",
        tags=["Users"]
        )
def create_user(user: User = Body(...)):
    """Create a User
    
    This Path operations creates a user in the app and save the infomation in the database

    Args:
        user (User, optional): USer ID. Defaults to Body(...).
    
    Returns:
        The infomation enter in the database by id 
    """
    
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    print(result)
    return'created'

#Update a User#
@user.put(
        path="/user/{id}/update",
        status_code=status.HTTP_201_CREATED,
        response_model=User,
        description=" Update a User by Id",
        tags=["Users"]
        )
def update_user(id: UUID = Path(...), user: User = Body(...)):
    """Update User
    
    This path operations modify the information of a user in the database

    Args:
        id (UUID, optional): user id. Defaults to Path(...).
        user (User, optional): user.name, user.email, user.password. Defaults to Body(...).

    Returns:
        201 (Created): if the information is correctly
    """
    conn.execute(users.update().values(name=user.name, email=user.email, password= user.password).where(users.c.id == id))
    return conn.execute(users.select().where(user.c.id == id)).firts()


#Delete a User#
@user.delete(
            path="/users/{id}/delete",
            response_model=User, 
            tags=["Users"],
            summary="Delete a User"
            )
def delete_user(id: UUID = Path(...)):
    """Delete a User
    
    This path operations Delete a user id the app

    Args:
        id (UUID, optional): User ID. Defaults to Path(...).

    Returns:
        NOT
    """
    conn.execute(users.delete().where(users.c.id == id))
    return "Delete"
    




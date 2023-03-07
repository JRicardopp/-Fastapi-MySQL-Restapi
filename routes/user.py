from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from config.db import conn, engine
from models.user import users
from schemas.user import User


from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users")
def get_users():
    return conn.execute(users.select()).fetchall()


@user.get("/users/count", tags=["users"], response_model=UserCount)
def get_users_count():
    result = conn.execute(select([func.count()]).select_from(users))
    return{"total": tuple(result)[0][0]}


@user.post("/",
           status_code=status.HTTP_201_CREATED
           )
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.put("/user/{id}/update")
def update_user():
    



@user.delete("/users/{id}/delete")
def delete_user():
    pass




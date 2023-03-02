from fastapi import APIRouter

user = APIRouter()

@user.post("/users")
def create_user():
    pass

@user.get("/users/{id}")
def show_user():
    pass

@user.delete("/users/{id}/delete")
def delete_user():
    pass

@user.put("/user/{id}/update")
def update_user():
    pass
from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from models import Gender, User, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(id=UUID("54a2cb90-7a9d-43a9-8922-0bd4b8b70cf5"),
         first_name="Jamila",
         last_name="Doe",
         middle_name="Laura",
         gender=Gender.female,
         roles=[Role.student]
         ),
    User(id=UUID("8ad94936-64dd-423f-a209-2469a175fa06"),
         first_name="Alex",
         last_name="Jones",
         middle_name="Rick",
         gender=Gender.male,
         roles=[Role.admin, Role.user]
         )
]


@app.get("/")
async def root():
    return {"Hello": "Les gens"}


@app.get("/api/v1/users")
async def fetch_users():
    return db;


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user);
    return {"id": user.id}


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} doesn't exists"
    )


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} doesn't exists"
    )

from fastapi import APIRouter, Body, Response, status, Path
from config.db import conn
from models.user import users
from schemas.user import User


user = APIRouter()

# get users


@user.get(
    path="/users",
    tags=["user"],
    response_model=list[User],
    status_code=status.HTTP_200_OK,
    summary="GET USERS"
)
def get_users():
    """
        - show users

        - This route operation shows all users

        - return a list of users with:
            - name
            - email
            - password

    """
    return conn.execute(users.select()).fetchall()

# create user


@user.post(
    path="/users",
    tags=["user"],
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="CREATE USERS"
)
def create_user(user: User):
    """
        - Create users

        - This route operation creates a user in the application and saves the information to the database.

        - parameters
            - Request body parameter:
                - **user** -> user model with:
                    - name
                    - email
                    - password
        - returns a users model with:
            - name
            - email
            - password
    """
    new_user = {"name": user.name, "email": user.email}
    new_user['password'] = user.password
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

# get user


@user.get(
    path="/users/{user_id}",
    tags=["user"],
    summary="GET A USER",
    response_model=User,
    status_code=status.HTTP_200_OK
)
def get_user(
    user_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    )
):
    """
         - show a user

        - This route operation show a user

        - returns a user model with:
            - name
            - email
            - password
    """
    return conn.execute(users.select().where(users.c.id == user_id)).first()

# delete user


@user.delete(
    path="/users/{user_id}",
    tags=["user"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="DELETE USER"
)
def delete_user(
    user_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    )
):
    """
        - delete user

        - This route operation removes a user from the application and saves the information to the database.

        - parameters
            - path parameter:
                - **user_id** 
            - Request body parameter:
                - **user** -> user model with:
                    - name
                    - email
                    - password
        - return a status
    """
    conn.execute(users.delete().where(users.c.id == user_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update user


@user.put(
    path="/users/{user_id}",
    tags=["user"],
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="UPDATE USER"
)
def update_user(
    user_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    user: User = Body(...)
):
    """
        - Update User

        - This route operation updates a user in the application and saves the information to the database.

        - parameters
            - path parameter:
                - **user_id** 
            - Request body parameter:
                - **user** -> user model with:
                    - name
                    - email
                    - password
        - returns a users model with:
            - name
            - email
            - password
    """
    conn.execute(users.update().values(name=user.name,
                 email=user.email, password=user.password).where(users.c.id == user_id))
    return conn.execute(users.select().where(users.c.id == user_id)).first()

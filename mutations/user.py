from ariadne import convert_kwargs_to_snake_case
from models.user import User
from datetime import datetime


@convert_kwargs_to_snake_case
def create_user_resolver(
    obj, info, username: str, email: str, password: str, role: str = "User"
):
    # today = date.today()
    hashed_password = User.generate_hash(password)
    if User.find_by_email(email) or User.find_by_username(username):
        raise ValueError("Email or Username Already exist")
    new_user = User(
        username=username,
        email=email,
        role=role,
        password=hashed_password,
        created_at=datetime.now(),
    )
    new_user.save()

    try:
        payload = {"user": new_user.to_dict(), "success": True}
    except ValueError:
        payload = {
            "success": False,
            "errors": [
                f"Incorrect date format provided, date format should be dd-mm-yyyy"
            ],
        }
    return payload


@convert_kwargs_to_snake_case
def update_post_resolver(
    obj, info, user_id: str, username: str, email: str, role: str, password: str
) -> dict:
    # Check if the post already exists
    user = User.query.get(user_id)
    try:
        user.username = username
        user.email = email
        user.password = password
        user.role = role
        user.update()
        payload = {"user": user.to_dict(), "success": True}

    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Cannot update!, a post with id {user_id} not found"],
        }

    return payload


@convert_kwargs_to_snake_case
def delete_user(obj, info, user_id: str) -> dict:
    try:
        user = User.query.get(user_id)
        user.delete()
        payload = {"user": user.to_dict(), "success": True}
    except AttributeError:
        payload = {"success": False, "errors": [f"Not Found"]}
    return payload

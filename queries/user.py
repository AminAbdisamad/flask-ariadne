from ariadne import convert_kwargs_to_snake_case
from models.user import User


def list_users_resolver(obj, info) -> dict:
    try:
        users = [user.to_dict() for user in User.query.all()]
        print(users)
        payload = {"success": True, "users": users}
    except Exception as Error:
        payload = {"success": False, "Error": [str(Error)]}
    return payload


@convert_kwargs_to_snake_case
def get_user_resolver(obj, info, user_id: str) -> dict:
    try:
        user = User.query.get(user_id)
        payload = {"user": user.to_dict(), "success": True}
    except AttributeError:
        payload = {"errors": [f"user with id {user_id} not found"], "success": False}
    return payload

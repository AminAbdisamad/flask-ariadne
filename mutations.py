from ariadne import convert_kwargs_to_snake_case
from model import Post
from datetime import datetime
from init import db


@convert_kwargs_to_snake_case
def create_post_resolver(obj, info, title: str, description: str):
    # today = date.today()
    new_post = Post(title=title, description=description, created_at=datetime.now())
    new_post.save()
    try:
        payload = {"post": new_post.to_dict(), "success": True}
    except ValueError:
        payload = {
            "success": False,
            "errors": [
                f"Incorrect date format provided, date format should be dd-mm-yyyy"
            ],
        }
    return payload


@convert_kwargs_to_snake_case
def update_post_resolver(obj, info, id: str, title: str, description: str) -> dict:
    # Check if the post already exists
    post = Post.query.get(id)
    try:
        post.title = title
        post.description = description
        post.update()
        payload = {"post": post.to_dict(), "success": True}

    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Cannot update!, a post with id {id} not found"],
        }

    return payload


def delete_post(obj, info, id: str) -> dict:
    try:
        post = Post.query.get(id)
        post.delete()
        payload = {"post": post.to_dict(), "success": True}
    except AttributeError:
        payload = {"success": False, "errors": [f"Not Found"]}
    return payload

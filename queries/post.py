from ariadne import convert_kwargs_to_snake_case
from models.post import Post


def list_posts_resolver(obj, info) -> dict:
    try:
        posts = [post.to_dict() for post in Post.query.all()]
        print(posts)
        payload = {"success": True, "posts": posts}
    except Exception as Error:
        payload = {"success": False, "Error": [str(Error)]}
    return payload


@convert_kwargs_to_snake_case
def getPost_resolver(obj, info, post_id: str) -> dict:
    try:
        post = Post.query.get(post_id)
        payload = {"post": post.to_dict(), "success": True}
    except AttributeError:
        payload = {"errors": [f"Post with id {post_id} not found"], "success": False}
    return payload

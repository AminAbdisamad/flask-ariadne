from model import Post


def list_posts_resolver(obj, info) -> dict:
    try:
        posts = [post.to_dict() for post in Post.query.all()]
        print(posts)
        payload = {"success": True, "posts": posts}
    except Exception as Error:
        payload = {"success": False, "Error": [str(Error)]}
    return payload

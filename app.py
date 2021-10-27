from flask import request, jsonify
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    ObjectType,
    snake_case_fallback_resolvers,
)
from ariadne.constants import PLAYGROUND_HTML
from queries.post import list_posts_resolver, getPost_resolver
from queries.user import list_users_resolver, get_user_resolver
from mutations.post import create_post_resolver, update_post_resolver, delete_post
from mutations.user import create_user_resolver, update_post_resolver, delete_user
from mutations.login import login_resolver
from init import app

# QUERIES
query = ObjectType("Query")
# Post Queries
query.set_field("listPosts", list_posts_resolver)
query.set_field("getPost", getPost_resolver)
# User Queries
query.set_field("listUsers", list_users_resolver)
query.set_field("getUser", get_user_resolver)


# MUTATIONS
mutation = ObjectType("Mutation")
# Post Mutations
mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post)
# User Mutations
mutation.set_field("createUser", create_user_resolver)
mutation.set_field("updateUser", update_post_resolver)
mutation.set_field("deleteUser", delete_user)

# Auth
mutation.set_field("Login", login_resolver)


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.get("/graphql")
def index():
    return PLAYGROUND_HTML, 200


@app.post("/graphql")
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)

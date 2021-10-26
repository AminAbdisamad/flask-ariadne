from flask import request, jsonify
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    ObjectType,
    snake_case_fallback_resolvers,
)
from ariadne.constants import PLAYGROUND_HTML
from queries import list_posts_resolver, getPost_resolver
from mutations import create_post_resolver, update_post_resolver, delete_post

from init import app

# QUERIES
query = ObjectType("Query")
query.set_field("listPosts", list_posts_resolver)
query.set_field("getPost", getPost_resolver)

# MUTATIONS
mutation = ObjectType("Mutation")
mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post)

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

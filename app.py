from flask import request, jsonify
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    ObjectType,
    snake_case_fallback_resolvers,
)
from ariadne.constants import PLAYGROUND_HTML
from queries import list_posts_resolver
from init import app


query = ObjectType("Query")
query.set_field("listPosts", list_posts_resolver)


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, query, snake_case_fallback_resolvers)


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

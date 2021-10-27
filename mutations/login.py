import datetime
from flask import request, jsonify, make_response
from ariadne import convert_kwargs_to_snake_case
from flask_jwt_extended import (
    verify_jwt_in_request,
    # get_jwt_claims,
    create_access_token,
    create_refresh_token,
    jwt_required,
    # jwt_refresh_token_required,
    get_jwt_identity,
    get_jti,
)
from functools import wraps
from models.user import User, RevokedTokenModel
from init import db, jwt

"""TODO:
get authorization header from the react app
and verify then allow it to access
token = request.headers['authorization'].split(" ")[1]
verify_jwt_token(token,'access_token')
then do staff
 """

# Custome JWT Decorator For Admin Users


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        admin = User.query.filter_by(name="Admin").first()
        # Check if if the current user is Admin
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        # Only then this we can perform admin tasks
        if current_user.role == admin:
            return fn(*args, **kwargs)
        else:
            return {"msg": "You're NOT allowed to perform this action!"}, 403

    return wrapper


# Check Blacklisted Tokens
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return RevokedTokenModel.is_jti_blacklisted(jti)


@convert_kwargs_to_snake_case
def login_resolver(obj, info, email: str, password: str):
    current_user = User.find_by_email(email)
    # Check if email exists
    if not current_user:
        return {"message": "Invalid email or password"}
    # Check if current user's password matches hashed password
    if User.verify_hash(current_user.password, password):
        print("SUCCESS - Verification - ")

        # Create Access token if user created successfully
        # !Access token we need to access protected routes.
        #! Refresh token we need to reissue access token when it will expire.
        try:
            expires = datetime.timedelta(days=5)
            # Token Expiration
            payload = {"payload": {"role": current_user.role, "id": current_user.id}}
            access_token = create_access_token(identity=payload, expires_delta=expires)
            refresh_token = create_refresh_token(identity=current_user.id)

            # Setting cookies in the browser
            response = make_response()
            response.set_cookie("access_token", access_token)
            response.set_cookie("refresh_token", refresh_token)

            data = {
                "success": True,
                "role": current_user.role,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        except Exception:
            data = {"success": False, "errors": ["Invalid email or password"]}
    return data


@jwt_required
def logout(obje, info):
    jti = get_jti()["jti"]
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {"success": True, "message": "Access token has been revoked"}, 200
    except:
        return {"success": False, "message": "Something went wrong"}, 500


# class UserLogoutRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         jti = get_raw_jwt()["jti"]
#         try:
#             revoked_token = RevokedTokenModel(jti=jti)
#             revoked_token.add()
#             return {"message": "Refresh token has been revoked"}
#         except:
#             return {"message": "Something went wrong"}, 500


# class TokenRefresh(Resource):
#     """
#     tokens have an expiration date. By default, access tokens have 15 minutes lifetime,
#     refresh tokens — 30 days. In order not to ask users to log in too often after access
#     token expiration we can reissue new access token using refresh token
#     """

#     @jwt_refresh_token_required
#     def post(self):
#         """
#         first of all, this resource has jwt_refresh_token_required decorator,
#         which means that you can access this path only using refresh token.
#         By the way, you cannot access jwt_required endpoints using refresh token,
#         and you cannot access jwt_refresh_token_required endpoints using access token.
#         This adds an additional layer of security. To identify user we use helper
#         function get_jwt_identity() which extract identity from refresh token.
#         Then we use this identity to generate a new access token and return it to the user.
#         """
#         current_user = get_jwt_identity()
#         access_token = create_access_token(identity=current_user)
#         return {"access_token": access_token}


# class SecretResource(Resource):
#     @jwt_required
#     def get(self):
#         return {"answer": 42}

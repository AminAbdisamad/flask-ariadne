from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Get Database Details from .env file
# dbName = os.getenv("DB_NAME")
# dbUser = os.getenv("DB_USERNAME")
# dbPassword = os.getenv("DB_PASSWORD")

# Init App
app = Flask(__name__)
# Init Bcrypt
# bcrypt = Bcrypt(app)
# app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")
# # blacklisting TOKENS   When Users LoggedOut
# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# More setup for JWT Security
# app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/v1.0/'
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/logout/access'
# app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# Securing Session cookies

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
)


# Init Json Web Token
# jwt = JWTManager(app)

# DB Configuration
# # SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{dbUser}:{dbPassword}@localhost/{dbName}"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_ariadne.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# mm = Marshmallow(app)

# # Configure Flask Migrate
# migrate = Migrate(app, db)


# We want to create all tables
@app.before_first_request
def create_tables():
    db.create_all()

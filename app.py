from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_ariadne.db"

db = SQLAlchemy(app)


@app.get("/")
def index():
    return "Hello there"


if __name__ == "__main__":
    app.run(debug=True)


from datetime import datetime
from model import Post

current_date = datetime.today().date()
new_post = Post(
    title="A new morning", description="A new morning details", created_at=current_date
)
db.session.add(new_post)
db.session.commit()

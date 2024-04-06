from flask import Flask,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:shubham01@localhost/flask_projects"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class user_data(db.Model):
    user_id = db.Column(db.String(100),primary_key = True)
    password = db.Column(db.String(20),nullable = False)
    email_id = db.Column(db.String(30),nullable = False)
    def __repr__(self) -> str:
        return f"{self.user_id}-{self.password}"
with app.app_context():
    db.create_all()
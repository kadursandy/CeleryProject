from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:today123@localhost:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String)


if __name__ == '__main__':
    app.run(debug=True)

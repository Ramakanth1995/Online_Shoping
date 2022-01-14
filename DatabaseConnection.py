'''from flask import Flask
from flask_mysqldb import MySQL


def conneciton(app):
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'grocery'

    return app'''

# importing libraries
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy


# creating an instance of the flask app
app = Flask(__name__)

# Configure our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

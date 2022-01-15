from settings import *

db = SQLAlchemy(app)


class Grocery_table(db.Model):
    __tablename__ = 'Grocery_tables'  # creating a table name #Grocery_tablelist
    Item_No = db.Column(db.Integer, primary_key=True)  # this is the primary key
    Item_Name = db.Column(db.String(80), nullable=False)
    Quantity_Remain  = db.Column(db.Integer)
    Item_Cost  = db.Column(db.Integer)
    Manufactured_By  = db.Column(db.String(80), nullable=False)
    Item_Type  = db.Column(db.String(80), nullable=False)
    Item_Code  = db.Column(db.String(80), nullable=False)


class Login(db.Model):
    __tablename__ = 'Grocery_tables'  # creating a table name #Grocery_tablelist

    username = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Integer, primary_key=True)
    currently_loggedin = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Integer, primary_key=True)


class Cart(db.Model):
    __tablename__ = 'Grocery_tables'  # creating a table name #Grocery_tablelist
    item_code = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Integer, primary_key=True)

class Order_history(db.Model):
    __tablename__ = 'Grocery_tables'  # creating a table name #Grocery_tablelist
    email_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, primary_key=True)
    item_Name = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.Integer, primary_key=True)
    total_cose = db.Column(db.Integer, primary_key=True)
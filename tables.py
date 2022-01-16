from settings import *

db = SQLAlchemy(app)
login_table_dataa = SQLAlchemy(app)
cart_table_dataa= SQLAlchemy(app)
order_history_dataa = SQLAlchemy(app)

class Grocery_table(db.Model):
    __tablename__ = 'Grocery_tables'  # creating a table name #Grocery_tablelist
    Item_No = db.Column(db.Integer, primary_key=True)  # this is the primary key
    Item_Name = db.Column(db.String(80), nullable=False)
    Quantity_Remain  = db.Column(db.Integer)
    Item_Cost  = db.Column(db.Integer)
    Manufactured_By  = db.Column(db.String(80), nullable=False)
    Item_Type  = db.Column(db.String(80), nullable=False)
    Item_Code  = db.Column(db.String(80), nullable=False)


class Login_table_dataa(login_table_dataa.Model):
    item_number = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email_id = db.Column(db.String(80))
    is_admin = db.Column(db.String(80))
    currently_loggedin = db.Column(db.String(80))
    created_time = db.Column(db.Date)
    is_active = db.Column(db.String(80))
    password = db.Column(db.String(80))


class Cart_table_dataa(cart_table_dataa.Model):
    item_number  = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.String(80))
    email = db.Column(db.String(80))

class Order_history_dataa(order_history_dataa.Model):
    item_number = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(80))
    order_id = db.Column(db.String(80))
    item_Name = db.Column(db.String(80))
    item_code = db.Column(db.String(80))
    total_cost = db.Column(db.Integer)


login_table_dataa.create_all()
cart_table_dataa.create_all()
order_history_dataa.create_all()


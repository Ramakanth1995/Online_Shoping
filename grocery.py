from settings import *
import json
# Initializing our database
from tables import Cart_table_dataa, cart_table_dataa

db = SQLAlchemy(app)


# the class Grocery_table will inherit the db.Model of SQLAlchemy


class Grocery_table(db.Model):
    __tablename__ = 'Grocery_tables'  # creating a table name #Grocery_tablelist
    Item_No = db.Column(db.Integer, primary_key=True)  # this is the primary key
    Item_Name = db.Column(db.String(80), nullable=False)
    Quantity_Remain  = db.Column(db.Integer)
    Item_Cost  = db.Column(db.Integer)
    Manufactured_By  = db.Column(db.String(80), nullable=False)
    Item_Type  = db.Column(db.String(80), nullable=False)
    Item_Code  = db.Column(db.String(80), nullable=False)

    def json(self):
        return {'Item_No': self.Item_No, 'Item_Name': self.Item_Name,
                'Quantity_Remain': self.Quantity_Remain, 'Item_Cost': self.Item_Cost,
                'Manufactured_By': self.Manufactured_By,'Item_Type': self.Item_Type,'Item_Code': self.Item_Code}
    def cart_json(self):
        return {'item_number': self.item_number, 'item_code': self.item_code,'email': self.email}

    def add_Grocery_table(_Item_Name,_Quantity_Remain,_Item_Cost,_Manufactured_By,_Item_Type,_Item_Code):
        '''function to add Grocery_table to database using _title, _year, _genre
        as parameters'''
        # creating an instance of our Grocery_table constructor
        new_Grocery_table = Grocery_table(Item_Name = _Item_Name,Quantity_Remain = _Quantity_Remain,Item_Cost = _Item_Cost,Manufactured_By= _Manufactured_By,Item_Type = _Item_Type,Item_Code = _Item_Code)
        db.session.add(new_Grocery_table)  # add new Grocery_table to database session
        db.session.commit()  # commit changes to session

    def add_cart_table(item_code,email):
        new_cart_table = Cart_table_dataa(item_code = item_code,email = email)
        cart_table_dataa.session.add(new_cart_table)
        cart_table_dataa.session.commit()

    def get_all_Grocery_tables(self):
        '''function to get all Grocery_tables in our database'''
        #db.create_all()
        return [Grocery_table.json(grocery_table) for grocery_table in Grocery_table.query.all()]

        #return Grocery_table.query.all()

    def get_Grocery_table(_Item_No):
        '''function to get Grocery_table using the Item_No of the Grocery_table as parameter'''
        return [Grocery_table.json(Grocery_table.query.filter_by(Item_Code=_Item_No).first())]
        # Grocery_table.json() coverts our output to json
        # the filter_by method filters the query by the Item_No
        # the .first() method displays the first value

    def update_Grocery_table(_Item_No, _title, _year, _genre):
        '''function to update the details of a Grocery_table using the Item_No, title,
        year and genre as parameters'''
        Grocery_table_to_update = Grocery_table.query.filter_by(Item_No=_Item_No).first()
        Grocery_table_to_update.title = _title
        Grocery_table_to_update.year = _year
        Grocery_table_to_update.genre = _genre
        db.session.commit()

    def delete_Grocery_table(_Item_No):
        '''function to delete a Grocery_table from our database using
           the Item_No of the Grocery_table as a parameter'''
        Grocery_table.query.filter_by(Item_No=_Item_No).delete()
        # filter by Item_No and delete
        db.session.commit()  # commiting the new change to our database
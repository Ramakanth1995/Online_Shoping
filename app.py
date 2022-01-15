from flask import render_template

from grocery import *
from datetime import datetime

Grocery_tablelist_records = None
c_names = None
# route to get all Grocery_tables
@app.route('/', methods=['GET', 'POST','PUT','DELETE'])
def get_Grocery_tables():
    global Grocery_tablelist_records,c_names
    '''Function to get all the Grocery_tables in the database'''
    #d = jsonify({'Grocery_tables': Grocery_table.get_all_Grocery_tables(1)})
    Grocery_tablelist_records = Grocery_table.get_all_Grocery_tables(1)
    print(Grocery_tablelist_records)
    c_names = Grocery_tablelist_records[0].keys()
    #return jsonify({'Grocery_tables': Grocery_table.get_all_Grocery_tables(1)})
    return render_template('index.html', name=Grocery_tablelist_records,column_names = c_names)



# route to get Grocery_table by Item_No
'''@app.route('/Grocery_tables/<int:Item_No>', methods=['GET', 'POST','PUT','DELETE'])
def get_Grocery_table_by_Item_No(Item_No):
    return_value = Grocery_table.get_Grocery_table(Item_No)
    return jsonify(return_value)'''


# route to add new Grocery_table
@app.route('/Grocery_tables', methods=['GET', 'POST','PUT','DELETE'])
def add_Grocery_table():
    global Grocery_tablelist_records, c_names

    #Item_Name,Quantity_Remain = Quantity_Remain,Item_Cost = Item_Cost,Expiry_Date = Expiry_Date,Manufactured_By= Manufactured_By,Item_Type = Item_Type,Item_Code = Item_Code
    request.method = 'POST'
    request_data = {}

    request_data["Item_Name"] = 'Sandwich Wheat'
    request_data["Quantity_Remain"] = 93
    request_data["Item_Cost"] = 9.99

    request_data["Manufactured_By"] = 'Essential Everyday '
    request_data["Item_Type"] = 'BREAD&BAKERY'
    request_data["Item_Code"] = 'BREAD-1478523690'

    Grocery_tablelist_records = Grocery_table.get_all_Grocery_tables(1)
    print(request_data)
    #request_data = request.get_json()  # getting data from client
    Grocery_table.add_Grocery_table(request_data["Item_Name"],request_data["Quantity_Remain"],request_data["Item_Cost"],request_data["Manufactured_By"],request_data["Item_Type"],request_data["Item_Code"])
    response = Response("Grocery_table added", 201, mimetype='application/json')
    return get_Grocery_tables()


# route to update Grocery_table with PUT method
Item_No_value = None
@app.route('/Grocery_tables/<int:Item_No>', methods=['GET', 'POST','PUT','DELETE'])
def update_Grocery_table(Item_No):
    global Item_No_value
    Item_No_value = Item_No
    return_value = Grocery_table.get_Grocery_table(Item_No)

    return render_template('Edit.html',data = return_value[0])

@app.route('/updated', methods=['GET', 'POST','PUT','DELETE'])
def updated():
    print(Item_No_value,'Item_No')
    global Grocery_tablelist_records, c_names
    request_data = {}
    request_data['title'] = request.form['title']
    request_data['year'] = request.form['year']
    request_data['genre'] = request.form['genre']

    Grocery_table.update_Grocery_table(Item_No_value, request_data['title'], request_data['year'], request_data['genre'])

    Grocery_tablelist_records = Grocery_table.get_all_Grocery_tables(1)

    return render_template('basic.html', name=Grocery_tablelist_records,column_names = c_names)

# route to delete Grocery_table using the DELETE method
@app.route('/Grocery_tabless/<int:Item_No>', methods=['GET', 'POST','PUT','DELETE'])
def remove_Grocery_table(Item_No):
    '''Function to delete Grocery_table from our database'''
    print(request.method,Item_No)

    if Item_No ==1 :
        response = Response("Item_No 1 we could not Deleted", status=200, mimetype='application/json')
    else:
        Grocery_table.delete_Grocery_table(Item_No)

    return get_Grocery_tables()


if __name__ == "__main__":
    db.create_all()
    app.run(port=1234, debug=True)
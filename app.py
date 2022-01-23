from flask import render_template
import sqlalchemy as db

from grocery import *
from settings import *
import json
cart_table = SQLAlchemy(app)

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

# route to add new Grocery_table
@app.route('/Grocery_tables', methods=['GET', 'POST','PUT','DELETE'])
def add_Grocery_table():
    global Grocery_tablelist_records, c_names

    '''#Item_Name,Quantity_Remain = Quantity_Remain,Item_Cost = Item_Cost,Expiry_Date = Expiry_Date,Manufactured_By= Manufactured_By,Item_Type = Item_Type,Item_Code = Item_Code
    request.method = 'POST'
    request_data = {}
    request_data["Item_Name"] = i[0]
    request_data["Quantity_Remain"] = i[1]
    request_data["Item_Cost"] = i[2]

    request_data["Manufactured_By"] = i[3]
    request_data["Item_Type"] = i[4]
    request_data["Item_Code"] = i[5]

    Grocery_tablelist_records = Grocery_table.get_all_Grocery_tables(1)
    print(request_data)
    # request_data = request.get_json()  # getting data from client
    Grocery_table.add_Grocery_table(request_data["Item_Name"], request_data["Quantity_Remain"],
                                    request_data["Item_Cost"], request_data["Manufactured_By"],
                                    request_data["Item_Type"], request_data["Item_Code"])
        

    #response = Response("Grocery_table added", 201, mimetype='application/json')'''
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

'''@app.route('/Grocery_tabless/<int:Item_No>', methods=['GET', 'POST','PUT','DELETE'])
def remove_Grocery_table(Item_No):

    Grocery_table.delete_Grocery_table(Item_No)

    return get_Grocery_tables()'''
User_Name = None
#login realted code
@app.route('/login', methods=['GET', 'POST'])
def login():
    global curently_login,loging_error_message,User_Name,User_Email,l
    valid_user = False
    if request.method == "POST":
        #User_Email = request.form.get("uname")
        uname = request.form.get("username")
        psw = request.form.get("password")
        print(uname, psw)

        s = [Grocery_table.login_json(grocery_table) for grocery_table in Login_table_dataa.query.all()]
        print(s,'l')
        for name in s:
            if uname in name.values():
                if psw == name['password']:
                    valid_user = True
                    User_Name = name['username']

        if valid_user == True:
            return render_template('index.html', name=Grocery_tablelist_records, column_names=c_names)
        else:
            return render_template('login.html')

    return render_template('login.html')

cart_items = []
checkout_price = 0

# route to get Grocery_table by Item_No
@app.route('/Grocery_tables/<int:Item_No>', methods=['GET', 'POST','PUT','DELETE'])
def get_Grocery_table_by_Item_No(Item_Code):
    return_value = Grocery_table.get_Grocery_table(Item_Code)
    cart_items.extend(return_value)
    return jsonify(return_value)
@app.route('/display', methods=['GET', 'POST'])
def display(records=None):
    global checkout_price
    price_list = []
    form_data = request.args.get('type')
    for c,price in enumerate(cart_items):
        if form_data in price.values():
            cart_items.pop(c)

    for price in cart_items:
        price_list.append(price['Item_Cost'])

    checkout_price = sum(price_list)

    return render_template('display.html', name=cart_items, price=sum(price_list), car_count=len(price_list))


@app.route('/cart',methods=['GET', 'POST'])
def cart():
    global form_data, l,curently_login,cart_items
    form_data = request.args.get('type')
    get_Grocery_table_by_Item_No(form_data)
    return render_template('index.html', name=Grocery_tablelist_records,column_names = c_names)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    if User_Name == None:
        return render_template('login.html')
    else:
        code = 0
        if checkout_price <= 0:
            return render_template('index.html', name=Grocery_tablelist_records, column_names=c_names)
        else:
            for i in cart_items:
                code = i['Item_Code']
            Grocery_table.add_cart_table(code, 'None')
            
    return render_template('checkout.html',name=cart_items,price = checkout_price)

@app.route('/invoice', methods=['GET', 'POST'])
def invoice():
    print(User_Name)
    email_id = User_Name
    order_id = 1
    print(cart_items)
    for i in cart_items:
        item_Name = i['Item_Name']
        item_code = i['Item_Code']
        total_cost = i['Item_Cost']

    Grocery_table.add_orderhistory_table( email_id,order_id,item_Name,item_code,total_cost)
    
    cart_items.clear()

    return render_template('index.html', name=Grocery_tablelist_records,column_names = c_names)


@app.route('/register',methods=['GET', 'POST'])
def register():
    global form_data, l,curently_login
    # User_Email = request.form.get("uname")
    username = request.form.get("username")
    Email = request.form.get("email")
    psw = request.form.get("password")
    psw2 = request.form.get("pass")
    if  Email or psw or psw2:
        Grocery_table.add_login_table(username, Email, psw)
        s = [Grocery_table.login_json(grocery_table) for grocery_table in Login_table_dataa.query.all()]
        return render_template('index.html', name=Grocery_tablelist_records,column_names = c_names)

    else:
        return render_template('register.html')

    return render_template('register.html')

@app.route('/order_history', methods=['GET', 'POST'])
def order_history():
    global order_history_records
    order_history_records = []
    #d = [Grocery_table.history_json(Order_history_dataa.query.filter_by(email_id='demo').first())]

    d = [Grocery_table.history_json(grocery_table) for grocery_table in Order_history_dataa.query.all()]

    print(d,'d')

    for i in d:
        if User_Name == i['email_id']:
            order_history_records.append(i)
    print(order_history_records)

    return render_template('order_history.html',records = order_history_records)

name = None
@app.route('/s/<name>', methods=['GET', 'POST'])
def product_overview(name):

    return render_template('/product_overview.html')

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    global curently_login,car_count,User_Name,name,names,l
    User_Name = None

    return render_template('index.html', name=Grocery_tablelist_records,column_names = c_names)

@app.route('/<name>', methods=['GET', 'POST'])
def add(name):

    return render_template( 'drwopdown.html')
if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)

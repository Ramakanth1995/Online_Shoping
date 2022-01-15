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
@app.route('/Grocery_tabless/<int:Item_No>', methods=['GET', 'POST','PUT','DELETE'])
def remove_Grocery_table(Item_No):
    '''Function to delete Grocery_table from our database'''
    print(request.method,Item_No)

    if Item_No ==1 :
        response = Response("Item_No 1 we could not Deleted", status=200, mimetype='application/json')
    else:
        Grocery_table.delete_Grocery_table(Item_No)

    return get_Grocery_tables()

#login realted code
@app.route('/login', methods=['GET', 'POST'])
def login():
    global curently_login,loging_error_message,User_Name,User_Email,l
    if request.method == "POST":

        #User_Email = request.form.get("uname")
        uname = request.form.get("username")
        psw = request.form.get("password")
        print(uname, psw)
        '''request.method == "GET"
        cur = mysql.connection.cursor()
        query_string = "SELECT * FROM login WHERE email_id = %s"
        cur.execute(query_string, (uname,))
        cur.connection.commit()
        login_details = cur.fetchall()
        cart_records = mysql.connection.cursor()
        if len(login_details)>=1:
            if uname == login_details[0][1] and psw == login_details[0][6]:
                curently_login = True
                User_Name = login_details[0][0]
                User_Email = login_details[0][1]
                if curently_login == True:
                    q = "select item_code from cart where email = %s;"
                    cart_records.execute(q, (User_Name,))
                    cart_records.connection.commit()
                    cart_records = cart_records.fetchall()

                    for rows in cart_records:
                        l.append(rows[0])
                    k = set(l)
                    l = list(k)

                return render_template('index.html', name=grocerylist_records, names=grocerylist_recordss,
                                       car_count=len(l),User_Name = User_Name)
            else:
                loging_error_message = "user name and password is not mateching please try again"

                return render_template('login.html', loging_error_message=loging_error_message)'''

    return render_template('login.html')
cart_items = []
cart_items_list = []
# route to get Grocery_table by Item_No
@app.route('/Grocery_tables/<int:Item_No>', methods=['GET', 'POST','PUT','DELETE'])
def get_Grocery_table_by_Item_No(Item_Code):
    return_value = Grocery_table.get_Grocery_table(Item_Code)
    cart_items.append(return_value)
    return jsonify(return_value)

@app.route('/display', methods=['GET', 'POST'])
def display(records=None):
    return render_template('display.html', name=cart_items, price=10, car_count=2)


@app.route('/cart',methods=['GET', 'POST'])
def cart(records=None):
    global form_data, l,curently_login,cart_items

    form_data = request.args.get('type')
    r = get_Grocery_table_by_Item_No(form_data)
    return render_template('index.html', name=Grocery_tablelist_records,column_names = c_names)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout(records=None):

    return render_template('checkout.html')


@app.route('/register',methods=['GET', 'POST'])
def register(records=None):
    global form_data, l,curently_login

    form_data = request.args.get('type')

    print(form_data)
    response = Response(form_data, 201, mimetype='application/json')
    return render_template('register.html')

app.route('/order_history', methods=['GET', 'POST'])
def order_history():
    global order_history_records

    return render_template('order_history.html')

name = None
@app.route('/s/<name>', methods=['GET', 'POST'])
def product_overview(name):

    return render_template('/product_overview.html')

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    global curently_login,car_count,User_Name,name,names,l


    return render_template('index.html')

@app.route('/<name>', methods=['GET', 'POST'])
def add(name):

    return render_template( 'drwopdown.html')
if __name__ == "__main__":
    db.create_all()
    app.run(port=1234, debug=True)
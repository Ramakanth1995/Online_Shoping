from email.mime.text import MIMEText

from flask import Flask, render_template, request

from DatabaseConnection import conneciton

from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import datetime;

app = Flask(__name__)
app  = conneciton(app)
mysql = MySQL(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pawwan431@gmail.com'
app.config['MAIL_PASSWORD'] = 'python@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
l=[]
form_data = None
grocerylist_records = None
grocerylist_recordss = None
curently_login = False
loging_error_message = None

User_Name = None

@app.route('/')
def home():
    global grocerylist_records,grocerylist_recordss,l
    if request.method == "GET":
        request.method == "GET"
        cur = mysql.connection.cursor()
        curr = mysql.connection.cursor()
        cur.execute("select * from grocerylist;")
        curr.execute("select * from grocerylist;")
        curr.connection.commit()
        cur.connection.commit()
        grocerylist_records = cur.fetchall()
        grocerylist_recordss = curr.fetchall()
        #print(recordss)
    return render_template('index.html',name =grocerylist_records ,names = grocerylist_recordss,car_count = len(l),User_Name = User_Name)
    #return render_template('checkout.html')

    return render_template('index.html')

@app.route('/cart',methods=['GET', 'POST'])
def cart(records=None):
    global form_data, l
    if request.method == "GET":
        #form_data = request.form.get('id')
        form_data = request.args.get('type')
        l.append(form_data)
        request.method == "GET"
        cur = mysql.connection.cursor()
        curr = mysql.connection.cursor()
        cur.execute("select * from grocerylist;")
        cur.connection.commit()
        records  =cur.fetchall()
        return render_template('index.html', name=records,car_count = len(l),User_Name = User_Name)
    return render_template('index.html',name=records, car_count = len(l),User_Name = User_Name)

total_price = None
@app.route('/display', methods=['GET', 'POST'])
def display(records=None):
    global l,total_price
    selected_id = request.args.get('type')
    print(l)
    if selected_id in l:
        l.remove(selected_id)
        print(l)
    if request.method == "GET":
        cur = mysql.connection.cursor()
        #query = "select * from products where productCode IN %s" %str(l)
        id_tuple = tuple(l)

        if len(id_tuple) > 1:
            query = 'SELECT * FROM grocerylist WHERE Item_Code IN {};'.format(id_tuple)
            cur.execute(query)
        else:
            g = id_tuple[0]
            query_string = "SELECT * FROM grocerylist WHERE Item_Code = %s"
            cur.execute(query_string, (g,))

        cur.connection.commit()
        records  =cur.fetchall()
        s = 0
        for i in range(len(records)):
            #print(type(records[i][3]))
            s = s+ float(records[i][3])
        total_price = s
    return render_template('display.html',name =records ,price = s,car_count = len(l))
records_checkout = None
@app.route('/checkout', methods=['GET', 'POST'])
def checkout(records=None):


    if curently_login == True:
        global l, records_checkout
        selected_id = request.args.get('type')
        print(l)
        if selected_id in l:
            l.remove(selected_id)
            print(l)
        if request.method == "GET":
            cur = mysql.connection.cursor()
            # query = "select * from products where productCode IN %s" %str(l)
            id_tuple = tuple(l)

            if len(id_tuple) > 1:
                query = 'SELECT * FROM grocerylist WHERE Item_Code IN {};'.format(id_tuple)
                cur.execute(query)
            else:
                g = id_tuple[0]
                query_string = "SELECT * FROM grocerylist WHERE Item_Code = %s"
                cur.execute(query_string, (g,))

            cur.connection.commit()
            records = cur.fetchall()

            records_checkout = records
            s = 0
            for i in range(len(records)):
                # print(type(records[i][3]))
                s = s + float(records[i][3])
            # print(s)
    else:
        return render_template('login.html')

    return render_template('checkout.html',name =records ,price = s,car_count = len(l))

invoice_data = []
Tax = 0.075
Grand_total = None
@app.route('/invoice', methods=['GET', 'POST'])
def invoice():
    global invoice_data,Tax,total_price,Grand_total,l

    full_name = request.form.get("firstname")
    Email =request.form.get("email")
    Address =request.form.get("address")
    City =request.form.get("city")
    State =request.form.get("state")
    Zip =request.form.get("zip")

    invoice_data = [full_name,Email,Address,City,State,Zip]

    Tax = total_price*0.075

    Grand_total = Tax+total_price

    msg = Message('Order successfully placed using FUCK.in', sender='pawwan431@gmail.com',
                  recipients=['amshala.srikanth438@gmail.com','ramakanth406@gmail.com'])

    msg.html = render_template( 'invoice.html',invoice_data =  invoice_data,records_checkout = records_checkout,total_price = total_price,Tax = Tax,Grand_total = Grand_total)
    mail.send(msg)

    l.clear()


    return render_template( 'invoice.html',invoice_data =  invoice_data,records_checkout = records_checkout,total_price = total_price,Tax = Tax,Grand_total = Grand_total)

@app.route('/<name>', methods=['GET', 'POST'])
def add(name):
    cur = mysql.connection.cursor()

    query_string = "SELECT * FROM grocerylist WHERE Item_Type = %s"

    cur.execute(query_string, (name,))
    cur.connection.commit()
    records = cur.fetchall()

    return render_template( 'drwopdown.html',name =records )


@app.route('/login', methods=['GET', 'POST'])
def login():
    global curently_login,loging_error_message,User_Name
    if request.method == "POST":
        print('login')
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        #print(uname, psw)
        request.method == "GET"
        cur = mysql.connection.cursor()
        query_string = "SELECT * FROM login WHERE email_id = %s"
        cur.execute(query_string, (uname,))
        cur.connection.commit()
        login_details = cur.fetchall()

        if len(login_details)>=1:
            if uname == login_details[0][1] and psw == login_details[0][6]:
                curently_login = True
                User_Name = login_details[0][0]
                return render_template('index.html', name=grocerylist_records, names=grocerylist_recordss,
                                       car_count=len(l),User_Name = User_Name)
            else:
                loging_error_message = "user name and password is not mateching please try again"

                return render_template('login.html', loging_error_message=loging_error_message)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global curently_login,loging_error_message,User_Name
    if request.method == "POST":
        Username = request.form.get("UserName")
        email = request.form.get("email")
        psw = request.form.get("psw")
        re_psw = request.form.get("psw-repeat")
        crated_date = datetime.datetime.now()
        #print(uname, psw)

        if psw == re_psw:
            request.method == "GET"
            cur = mysql.connection.cursor()
            query_string = "insert into login (username,email_id,created_time,password) values(%s,%s,%s,%s);"
            cur.execute(query_string, (Username,email,crated_date,psw))
            cur.connection.commit()
            #login_details = cur.fetchall()
            print('sucess')

            return render_template('login.html', loging_error_message=loging_error_message)

    return render_template('register.html')


@app.route('/order_history', methods=['GET', 'POST'])
def order_history():

    print(invoice_data)


    return render_template('order_history.html',invoice_data = invoice_data)

if __name__ == '__main__':

    app.run()


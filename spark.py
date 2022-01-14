from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///api.db')

table = db['customer']

def fetch_db(id):  
    return table.find_one(id=id)

def fetch_db_all():
    customer = []
    for book in table:
        customer.append(book)
    return customer

@app.route('/', methods=['GET'])
def db_populate():
    table.insert({"id": 1,"First Name": "pavan","Last Name": "Kumar",
        "Company Name": "sattrix.com",
        "Branch": "Ebranch"})

    table.insert({"id": 2, "First Name": "pavan", "Last Name": "Kumar",
                  "Company Name": "sattrix.com",
                  "Branch": "Ebranch"})

    return make_response(jsonify(fetch_db_all()),
                         200)

@app.route('/api/customer', methods=['GET', 'POST'])
def api_customer():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        id = content['id']
        table.insert(content)
        return make_response(jsonify(fetch_db(id)), 201)  # 201 = Created


@app.route('/api/customer/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_book(id):
    if request.method == "GET":
        book_obj = fetch_db(id)
        if book_obj:
            return make_response(jsonify(book_obj), 200)
        else:
            return make_response(jsonify(book_obj), 404)
    elif request.method == "PUT":  
        content = request.json
        table.update(content, ['id'])

        book_obj = fetch_db(id)
        return make_response(jsonify(book_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=id)

        return make_response(jsonify({}), 204)


if __name__ == '__main__':
    app.run(debug=True)
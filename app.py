from flask import render_template

from movies import *

grocerylist_records = None
c_names = None
# route to get all movies
@app.route('/', methods=['GET', 'POST','PUT','DELETE'])
def get_movies():
    global grocerylist_records,c_names
    '''Function to get all the movies in the database'''
    #d = jsonify({'Movies': Movie.get_all_movies(1)})
    grocerylist_records = Movie.get_all_movies(1)
    c_names = grocerylist_records[0].keys()
    #return jsonify({'Movies': Movie.get_all_movies(1)})
    return render_template('basic.html', name=grocerylist_records,column_names = c_names)



# route to get movie by id
'''@app.route('/movies/<int:id>', methods=['GET', 'POST','PUT','DELETE'])
def get_movie_by_id(id):
    return_value = Movie.get_movie(id)
    return jsonify(return_value)'''


# route to add new movie
@app.route('/movies', methods=['GET', 'POST','PUT','DELETE'])
def add_movie():
    global grocerylist_records, c_names
    '''Function to add new movie to our database'''
    print(request.method,'ad')
    request.method = "POST"
    print(request.method, 'ad')
    title = request.form['title']
    print(title)
    year = request.form['year']
    genre = request.form['genre']
    request.method = 'POST'
    request_data = {}
    request_data["title"] = title
    request_data["year"] = year
    request_data["genre"] = genre
    grocerylist_records = Movie.get_all_movies(1)

    #request_data = request.get_json()  # getting data from client
    Movie.add_movie(request_data["title"], request_data["year"],
                    request_data["genre"])
    response = Response("Movie added", 201, mimetype='application/json')
    return get_movies()


# route to update movie with PUT method
id_value = None
@app.route('/movies/<int:id>', methods=['GET', 'POST','PUT','DELETE'])
def update_movie(id):
    global id_value
    id_value = id
    return_value = Movie.get_movie(id)

    return render_template('Edit.html',data = return_value[0])

@app.route('/updated', methods=['GET', 'POST','PUT','DELETE'])
def updated():
    print(id_value,'id')
    global grocerylist_records, c_names
    request_data = {}
    request_data['title'] = request.form['title']
    request_data['year'] = request.form['year']
    request_data['genre'] = request.form['genre']

    Movie.update_movie(id_value, request_data['title'], request_data['year'], request_data['genre'])

    grocerylist_records = Movie.get_all_movies(1)

    return render_template('basic.html', name=grocerylist_records,column_names = c_names)

# route to delete movie using the DELETE method
@app.route('/moviess/<int:id>', methods=['GET', 'POST','PUT','DELETE'])
def remove_movie(id):
    '''Function to delete movie from our database'''
    print(request.method,id)

    if id ==1 :
        response = Response("Id 1 we could not Deleted", status=200, mimetype='application/json')
    else:
        Movie.delete_movie(id)

    return get_movies()


if __name__ == "__main__":
    db.create_all()
    app.run(port=1234, debug=True)
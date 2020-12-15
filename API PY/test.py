import flask
from flask import request, jsonify
import pyodbc

app = flask.Flask(__name__)
app.config["DEBUG"] = True

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=.\\;'
    'Database=ApartmentRentalDB;'
    'Trusted_Connection=yes;'
)

@app.route('/', methods=['GET'])
def home():
        
    return "<h1>snopp</h1>"

#GET ALL USERS
@app.route('/api/users', methods=['GET'])
def users():
    cur = conn.cursor()
    results = []
    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[User];').fetchall()
    
    response = []

    for user in results:
        response.append(
            {'Id': user.Id,
            'Username': user.Username,
            'Password': user.Password,
            'Landlord': user.Landlord}
        )
        
    return jsonify(response)

@app.route('/api/user', methods=['POST'])
def create_user():
    return "<h1>hej</h1>"

#LOGIN FUNCTION
#to do fixa 
@app.route('/api/login', methods=['GET'])
def login():

    if 'username' in request.args:
        username = (request.args['username'])
    else:
        return 'error no variable'

    if 'password' in request.args:
        password = (request.args['password'])
    else:
        return 'error no variable'

    to_filter = "Username = '" + username + "' AND " + "Password = '" + password + "'"
    cur = conn.cursor()
    results = []
    results = cur.execute('SELECT Username, Password FROM [ApartmentRentalDB].[dbo].[User] WHERE ' + to_filter).fetchall()

    if len(results) == 1:
        for row in results:
            if row.Username == username and row.Password == password:
                response = []
                response.append(
                    {"Username": row.Username,
                    "Password": row.Password}
                )

                return jsonify(response)
            else:
                responseError = {"error": "Username and password did not match"}
                return jsonify(responseError)

    responseError = {"error": "Could not find user, invalid username or password"}
    return jsonify(responseError)

app.run()
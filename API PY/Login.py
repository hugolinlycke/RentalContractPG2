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
        
    return "<h1>Main page</h1>"

#GET ALL USERS
@app.route('/api/read/user', methods=['GET'])
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

@app.route('/api/read/user/<id>', methods=['GET'])
def fetch_one_user(id):
    cur = conn.cursor()
    to_filter = 'Id = ' + id
    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE ' + to_filter + ';').fetchall()
    
    if len(results) > 0:
        for user in results:
            response = (
                {'Id': user.Id,
                'Username': user.Username,
                'Password': user.Password,
                'Landlord': user.Landlord}
            )
        
        return jsonify(response)
    else:
        return error_page(418, "User not found on id: " + id)
    

@app.route('/api/create/user', methods=['POST'])
def create_user():

    if request.json['Username'] != None and request.json['Landlord'] != None and request.json['Password'] != None:
        username = request.json['Username']
        password = request.json['Password']
        landlord = request.json['Landlord']

        cur = conn.cursor()

        results = cur.execute("SELECT Username FROM [ApartmentRentalDB].[dbo].[User] WHERE Username='" + username + "'").fetchall()
        
        
        if len(results) > 0:
            
            if results[0].Username == username:
                return error_page(418, 'Cannot be the same username')
        else:
            cur.execute("INSERT INTO [ApartmentRentalDB].[dbo].[User] (Username, Password, Landlord) VALUES ('"+username + "','" + password + "','" + str(landlord) +"');")
            conn.commit()
            results1 = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Username = '" + username + "';").fetchall()
            if len(results1) > 0:
                for user in results1:
                    response = (
                        {'Id': user.Id,
                        'Username': user.Username,
                        'Password': user.Password,
                        'Landlord': user.Landlord}
                    )
            return jsonify(response)
        
    else:
        return error_page(418, 'Username, password and landlord needs to be set')

#UPDATE FUNCTION, not able to change landlord status. Only able to do that in creation
@app.route('/api/update/user', methods=['PUT'])
def updateuser():

    if request.json['Id'] != None and request.json['Username'] != None and request.json['Password'] != None:
        userId = request.json['Id']
        username = request.json['Username']
        password = request.json['Password']
        

        cur = conn.cursor()

        cur.execute("UPDATE [ApartmentRentalDB].[dbo].[User] SET Username= '" + username + "'," + " Password= '" + password + "' WHERE Id= " + userId)
        conn.commit()
        return "<h1>Well shaken mojito!</h1>"

    else:
        return error_page(418, "Not all fields are filled out buddy")

@app.route('/api/delete/user/<Id>', methods=['DELETE'])
def deleteuser(Id):

    cur = conn.cursor()

    userInPointTable = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Point] WHERE UserId =" + Id)
    userInInterestTable = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] WHERE UserId =" + Id)
    userInOfferTable = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE UserId =" + Id)

    if len(userInPointTable) > 0:
        cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[Point] WHERE UserId = ' + Id)
    
    if len(userInInterestTable) > 0:
        cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[Interest] WHERE UserId = ' + Id)
    
    if len(userInOfferTable) > 0:
        cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE UserId = ' + Id)


    cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = ' + Id)
    conn.commit()
    return "<h1>Deleted! wow!</h1>"



@app.errorhandler(404)
def page_not_found(e):
    return  "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.errorhandler(418)
def error_page(e, text):
    return "<h1>418</h1><p>" + text + "</p>", 418

#LOGIN FUNCTION
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
    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE ' + to_filter).fetchall()

    if len(results) == 1:
        for row in results:
            if row.Username == username and row.Password == password:
                response = (
                    {"Id": row.Id,
                    "Username": row.Username,
                    "Password": row.Password,
                    "Landlord": row.Landlord}
                )

                return jsonify(response)
            else:
                return error_page(418, "Username and password does not match")

    return error_page(418, "Username and password does not match")

app.run()
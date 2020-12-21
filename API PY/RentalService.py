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

    if request.get_json(force=True)['Username'] != None and request.get_json(force=True)['Landlord'] != None and request.get_json(force=True)['Password'] != None:
        username = request.get_json(force=True)['Username']
        password = request.get_json(force=True)['Password']
        landlord = request.get_json(force=True)['Landlord']

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
    
    try: request.json['Id']
    except KeyError: return error_page(418, "Id not set")

    try: request.json['Username']
    except KeyError: return error_page(418, "Username not set")

    try: request.json['Password']
    except KeyError: return error_page(418, "Password not set")

    if request.get_json(force=True)['Id'] != None and request.get_json(force=True)['Username'] != None and request.get_json(force=True)['Password'] != None:
        userId = request.get_json(force=True)['Id']
        username = request.get_json(force=True)['Username']
        password = request.get_json(force=True)['Password']
            
        cur = conn.cursor()

        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id= " + userId).fetchall()


        if len(results) > 0:
            cur.execute("UPDATE [ApartmentRentalDB].[dbo].[User] SET Username= '" + username + "'," + " Password= '" + password + "' WHERE Id= " + userId)
            conn.commit()
            results1 = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id= " + userId).fetchall()
            for user in results1:
                response = (
                    {'Id': user.Id,
                    'Username': user.Username,
                    'Password': user.Password,
                    'Landlord': user.Landlord}
                )
            return jsonify(response)
        else:
            return error_page(418, "Could not find user")

    else:
        return error_page(418, "Not all fields are filled out buddy")

@app.route('/api/delete/user/<Id>', methods=['DELETE'])
def deleteuser(Id):

    cur = conn.cursor()

    results1 = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id =' + Id).fetchall()

    if len(results1) > 0:
        userInPointTable = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Point] WHERE UserId =" + Id).fetchall()
        userInInterestTable = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] WHERE UserId =" + Id).fetchall()
        userInOfferTable = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE UserId =" + Id).fetchall()

        if len(userInPointTable) > 0:
            cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[Point] WHERE UserId = ' + Id)
        
        if len(userInInterestTable) > 0:
            cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[Interest] WHERE UserId = ' + Id)
        
        if len(userInOfferTable) > 0:
            cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE UserId = ' + Id)


        cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = ' + Id)
        conn.commit()
        return "<h1>Deleted! wow!</h1>"
    else:
        return error_page(418, "User not found")

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




    #END OF LOGIN
    #NEW SERVICE

    #metoder ATT GÖRA
    #CRUD för apartment
    #Get specific apartment from apartment ID
    #Get specific apartment from landlord ID
    
    #CRUD för interest list
    #Get specific interest list from apartmentId
    #Get specific interest list from userid

    #CRUD för rental offer
    #Get specific rental offer with userID
    #Get sepcific rental offer with landlordId

    #CRUD för point
    #Get specific point from userId

    #Funktion för att poäng skall uppdateras automatisk efter en viss tid
    #Filter funktion sortera efter price (range ex 300-2000), location och size
    
    #Show similar apartment when clicked an apartment (restrictions -> location)

app.run()
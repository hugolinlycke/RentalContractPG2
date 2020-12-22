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
@app.route('/api/read/users', methods=['GET'])
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

    try: request.json['Id']
    except KeyError: return error_page(418, "Id not set")

    try: request.json['Username']
    except KeyError: return error_page(418, "Username not set")

    try: request.json['Password']
    except KeyError: return error_page(418, "Password not set")

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
        return error_page(418, 'error no variable')

    if 'password' in request.args:
        password = (request.args['password'])
    else:
        return error_page(418, 'error no variable')

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

#-------------------------------------------------------------------------------------------------------
#                                          END OF LOGIN SERVICE
#-------------------------------------------------------------------------------------------------------

#metoder ATT GÖRA
    
    #CRUD för interest list
    #Get specific interest list from apartmentId
    #Get specific interest list from userid

    #CRUD för rental offer
    #Get specific rental offer with userID
    #Get sepcific rental offer with landlordId

    #CRUD för point
    #Get specific point from userId

    #Funktion för att poäng skall uppdateras automatisk efter en viss tid

    
    


@app.route('/api/read/apartments', methods=['GET'])
def getApartments():
    cur = conn.cursor()
    results = []
    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment];').fetchall()
        
    response = []

    for apartment in results:
        response.append(
            {'Id': apartment.Id,
            'Price': apartment.Price,
            'NumberOfRooms': apartment.NumberOfRooms,
            'SizeOfApartment': apartment.SizeOfApartment,
            'Address': apartment.Address,
            'Location': apartment.Location,
            'Information': apartment.Information,
            'LandlordId': apartment.LandlordId,
            'Active': apartment.Active}
        )
        
    return jsonify(response)

@app.route('/api/read/apartment', methods=['GET'])
def getApartmentWithId():
    cur = conn.cursor()
    to_filter = []
    if 'id' in request.args:
        Id = (request.args['id'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")
        to_filter.append("Id = " + Id) 

    if 'landlordid' in request.args:
        LandlordId = (request.args['landlordid'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")
        to_filter.append("LandlordId =" + LandlordId)

    if 'active' in request.args:
        Active = (request.args['active'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")
        to_filter.append("Active = '" + str(Active) + "'") 

    strFilter = "WHERE "
    for x in to_filter:
        strFilter += x

    if len(to_filter) > 0:
        results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] ' + strFilter).fetchall()
        response = []

        if len(results) > 0:
            for apartment in results:
                response.append(
                    {'Id': apartment.Id,
                    'Price': apartment.Price,
                    'NumberOfRooms': apartment.NumberOfRooms,
                    'SizeOfApartment': apartment.SizeOfApartment,
                    'Address': apartment.Address,
                    'Location': apartment.Location,
                    'Information': apartment.Information,
                    'LandlordId': apartment.LandlordId,
                    'Active': apartment.Active}
                )
            
            return jsonify(response)
        else:
            return error_page(418, "Apartment not found")
    else:
        return error_page(418, "Need to use atleast one parameter")

@app.route('/api/create/apartment', methods=['POST'])
def createApartment():

    data = ['Id', 'Price', 'numberOfRooms', 'sizeOfApartment', 'Address',
    'Location', 'Information',  'LandlordId', 'Active']

    for x in data:
        try: request.json[x]
        except KeyError: return error_page(418, x + " not set")

    if request.json['Address'] != None and request.json['Location'] != None and request.json['LandlordId'] != None and request.json['Active'] != None:
        Price = request.json['Price']
        numberOfRooms = request.json['numberOfRooms']
        sizeOfApartment = request.json['sizeOfApartment']
        Address = request.json['Address']
        Location = request.json['Location']
        Information = request.json['Information']
        LandlordId = request.json['LandlordId']
        Active = request.json['Active']

        cur = conn.cursor()

        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(LandlordId)).fetchall()

        if len(results) > 0:
            cur.execute("INSERT INTO [ApartmentRentalDB].[dbo].[Apartment] (Price, numberOfRooms, sizeOfApartment, Address, Location, Information, LandlordId, Active) VALUES ("+ str(Price)  + ",'" + numberOfRooms + "','" + sizeOfApartment + "','" + Address + "','" + Location + "','" + Information + "'," + str(LandlordId) + ",'" + str(Active) +"');")
        conn.commit()
        results1 = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id = SCOPE_IDENTITY()").fetchall()
        if len(results1) > 0:
            for apartment in results1:
                response = (
                     {'Id': apartment.Id,
                    'Price': apartment.Price,
                    'NumberOfRooms': apartment.NumberOfRooms,
                    'SizeOfApartment': apartment.SizeOfApartment,
                    'Address': apartment.Address,
                    'Location': apartment.Location,
                    'Information': apartment.Information,
                    'LandlordId': apartment.LandlordId,
                    'Active': apartment.Active}
                )
            return jsonify(response)
        else:
            return error_page(418, "Landlord don't exist with id: " + LandlordId)
    else:
        return error_page(418, "Id, Address, location, landlord id and Active can't be NULL")

@app.route('/api/update/apartment', methods=['PUT'])
def updateApartment():
    
    data = ['Id', 'Price', 'numberOfRooms', 'sizeOfApartment', 'Address',
    'Location', 'Information',  'LandlordId', 'Active']

    for x in data:
        try: request.json[x]
        except KeyError: return error_page(418, x + " not set")

    if request.json['Id'] != None and request.json['Address'] != None and request.json['Location'] != None and request.json['LandlordId'] != None and request.json['Active'] != None:
        Id = request.json['Id']
        Price = request.json['Price']
        numberOfRooms = request.json['numberOfRooms']
        sizeOfApartment = request.json['sizeOfApartment']
        Address = request.json['Address']
        Location = request.json['Location']
        Information = request.json['Information']
        LandlordId = request.json['LandlordId']
        Active = request.json['Active']
            
        cur = conn.cursor()

        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id= " + str(Id)).fetchall()

        if len(results) > 0:
            cur.execute("UPDATE [ApartmentRentalDB].[dbo].[Apartment] SET Price= " + str(Price) + ", numberOfRooms= '" + numberOfRooms + "', sizeOfApartment ='" + sizeOfApartment + "', Address = '" + Address + "', Location ='" +  Location + "', Information = '" + Information + "', LandlordId = " + str(LandlordId) + ", Active = '" + str(Active) + "' WHERE Id= " + str(Id))
            conn.commit()
            results1 = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id= " + str(Id)).fetchall()
            for apartment in results1:
                response = (
                    {'Id': apartment.Id,
                    'Price': apartment.Price,
                    'NumberOfRooms': apartment.NumberOfRooms,
                    'SizeOfApartment': apartment.SizeOfApartment,
                    'Address': apartment.Address,
                    'Location': apartment.Location,
                    'Information': apartment.Information,
                    'LandlordId': apartment.LandlordId,
                    'Active': apartment.Active}
                )
            return jsonify(response)
        else:
            return error_page(418, "Could not find apartment")

    else:
        return error_page(418, "Not all fields are filled out buddy")

@app.route('/api/delete/apartment/<Id>', methods=['DELETE'])
def deleteApartment(Id):

    cur = conn.cursor()

    results1 = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id =' + Id).fetchall()

    if len(results1) > 0:
        apartmentInInterest = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] WHERE ApartmentId =" + Id).fetchall()
        apartmentInOffer = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE ApartmentId =" + Id).fetchall()

     
        if len(apartmentInInterest) > 0:
            cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[Interest] WHERE ApartmentId = ' + Id)
        
        if len(apartmentInOffer) > 0:
            cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE ApartmentId = ' + Id)


        cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id = ' + Id)
        conn.commit()
        return "<h1>Deleted! wow!</h1>"
    else:
        return error_page(418, "User not found")


@app.route('/api/read/apartment/similar')
def showSimilarApartment():

    if 'location' in request.args:
        Location = (request.args['location'])

        cur = conn.cursor()

        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Location = '" + Location + "';")

        response = []
        for apartment in results:
            response.append(
                    {'Id': apartment.Id,
                    'Price': apartment.Price,
                    'NumberOfRooms': apartment.NumberOfRooms,
                    'SizeOfApartment': apartment.SizeOfApartment,
                    'Address': apartment.Address,
                    'Location': apartment.Location,
                    'Information': apartment.Information,
                    'LandlordId': apartment.LandlordId,
                    'Active': apartment.Active}
                )
        return jsonify(response)

    else:
        return error_page(418, 'Invalid parameter or parameter not found')

#Filter funktion sortera efter price (range ex 300-2000), location och size
@app.route('/api/read/apartment/filter', methods=['GET'])
def filterApartments():
    cur = conn.cursor()
    to_filter = []
    if 'location' in request.args:
        Location = (request.args['location'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")
        to_filter.append("Location = '" + Location + "'") 

    if 'rooms' in request.args:
        rooms = (request.args['rooms'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")
        to_filter.append("NumberOfRooms ='" + rooms + "'")

    if 'minprice' in request.args and 'maxprice' in request.args:
        minprice = (request.args['minprice'])
        maxprice = (request.args['maxprice'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")

        to_filter.append("Price BETWEEN " + minprice + " AND " + maxprice)

    strFilter = "WHERE "
    for x in to_filter:
        strFilter += x

    if len(to_filter) > 0:
        results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] ' + strFilter).fetchall()
        response = []

        if len(results) > 0:
            for apartment in results:
                response.append(
                    {'Id': apartment.Id,
                    'Price': apartment.Price,
                    'NumberOfRooms': apartment.NumberOfRooms,
                    'SizeOfApartment': apartment.SizeOfApartment,
                    'Address': apartment.Address,
                    'Location': apartment.Location,
                    'Information': apartment.Information,
                    'LandlordId': apartment.LandlordId,
                    'Active': apartment.Active}
                )
            
            return jsonify(response)
        else:
            return error_page(418, "Apartments not found")
    else:
        results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment]').fetchall()
        response = []

        if len(results) > 0:
            for apartment in results:
                response.append(
                    {'Id': apartment.Id,
                    'Price': apartment.Price,
                    'NumberOfRooms': apartment.NumberOfRooms,
                    'SizeOfApartment': apartment.SizeOfApartment,
                    'Address': apartment.Address,
                    'Location': apartment.Location,
                    'Information': apartment.Information,
                    'LandlordId': apartment.LandlordId,
                    'Active': apartment.Active}
                )
            
            return jsonify(response)
        

app.run()
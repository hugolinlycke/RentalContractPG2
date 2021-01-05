import flask
from flask import request, jsonify
import pyodbc
import schedule
import time
import threading

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False


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
            'Picture': apartment.Picture,
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
                    'Picture': apartment.Picture,
                    'Active': apartment.Active}
                )
            
            return jsonify(response)
        else:
            return error_page(418, "Apartment not found")
    else:
        return error_page(418, "Need to use atleast one parameter")

@app.route('/api/create/apartment', methods=['POST'])
def createApartment():

    data = ['Price', 'numberOfRooms', 'sizeOfApartment', 'Address',
    'Location', 'Information',  'LandlordId', 'Picture', 'Active']

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
        Picture = request.json['Picture']

        cur = conn.cursor()

        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(LandlordId)).fetchall()
        if len(results) > 0:
            if results[0].Landlord == True:
                cur.execute("INSERT INTO [ApartmentRentalDB].[dbo].[Apartment] (Price, numberOfRooms, sizeOfApartment, Address, Location, Information, LandlordId, Active, Picture) VALUES ("+ str(Price)  + ",'" + numberOfRooms + "','" + sizeOfApartment + "','" + Address + "','" + Location + "','" + Information + "'," + str(LandlordId) + ",'" + str(Active) +"','" + Picture + "');")
                conn.commit()
                results1 = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id = SCOPE_IDENTITY()").fetchall()
            else:
                return error_page(418, "User is not landlord, id: " + str(LandlordId))
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
                    'Picture': apartment.Picture,
                    'Active': apartment.Active}
                )
            return jsonify(response)
        else:
            return error_page(418, "Landlord don't exist with id: " + str(LandlordId))
    else:
        return error_page(418, "Id, Address, location, landlord id and Active can't be NULL")

@app.route('/api/update/apartment', methods=['PUT'])
def updateApartment():
    
    data = ['Id', 'Price', 'numberOfRooms', 'sizeOfApartment', 'Address',
    'Location', 'Information',  'LandlordId', 'Picture','Active']

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
        Picture = request.json['Picture']
            
        cur = conn.cursor()

        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id= " + str(Id)).fetchall()
        userResults = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(LandlordId)).fetchall()

        if len(results) > 0 and len(userResults) > 0:
            if userResults[0].Landlord == True:
                cur.execute("UPDATE [ApartmentRentalDB].[dbo].[Apartment] SET Price= " + str(Price) + ", numberOfRooms= '" + numberOfRooms + "', sizeOfApartment ='" + sizeOfApartment + "', Address = '" + Address + "', Location ='" +  Location + "', Information = '" + Information + "', LandlordId = " + str(LandlordId) + ", Active = '" + str(Active) + "', Picture = '" + Picture + "' WHERE Id= " + str(Id))
                conn.commit()
            else:
                return error_page(418, "User is not landlord, id: " + str(LandlordId))
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
                    'Picture': apartment.Picture,
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
        return error_page(418, "Apartment not found")


@app.route('/api/read/apartment/similar', methods=['GET'])
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
                    'Picture': apartment.Picture,
                    'Active': apartment.Active}
                )
        return jsonify(response)

    else:
        return error_page(418, 'Invalid parameter or parameter not found')

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
                    'Picture': apartment.Picture,
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
                    'Picture': apartment.Picture,
                    'Active': apartment.Active}
                )
            
            return jsonify(response)
        
#-------------------------------------------------------------------------------------------------------
#                                          END OF APARTMENT SERVICE
#-------------------------------------------------------------------------------------------------------


@app.route('/api/read/interests', methods=['GET'])
def getAllInterests():
    cur = conn.cursor()
    results = []
    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Interest];').fetchall()
        
    response = []

    for interest in results:
        response.append(
            {'Id': interest.Id,
            'UserId': interest.UserId,
            'ApartmentId': interest.ApartmentId}
        )
        
    return jsonify(response)

@app.route('/api/read/interest', methods=['GET'])
def getSpecificInterest():
    cur = conn.cursor()
    to_filter = []
    if 'userid' in request.args:
        userId = (request.args['userid'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")
        to_filter.append("UserId = " + userId) 

    if 'apartmentid' in request.args:
        apartmentId = (request.args['apartmentid'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")
        to_filter.append("ApartmentId =" + apartmentId)

    strFilter = "WHERE "
    for x in to_filter:
        strFilter += x

    if len(to_filter) > 0:
        results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] ' + strFilter).fetchall()
        response = []

        if len(results) > 0:
            for interest in results:
                response.append(
                    {'Id': interest.Id,
                    'UserId': interest.UserId,
                    'ApartmentId': interest.ApartmentId}
                )
            
            return jsonify(response)
        else:
            return error_page(418, "Interest list not found")
    else:
        return error_page(418, "Need to use atleast one parameter")

@app.route('/api/create/interest', methods=['POST'])
def createInterest():
    
    data = ['UserId', 'ApartmentId']

    for x in data:
        try: request.json[x]
        except KeyError: return error_page(418, x + " not set")

    if request.json['UserId'] != None and request.json['ApartmentId']:
        userId = request.json['UserId']
        apartmentId = request.json['ApartmentId']
        

        cur = conn.cursor()

        userResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(userId)).fetchall()
        apartmentResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id = " + str(apartmentId)).fetchall()
        interestResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] WHERE UserId = " + str(userId)).fetchall()

        if len(userResult) > 0 and len(apartmentResult) > 0:
            if userResult[0].Landlord == False:
                if len(interestResult) <= 0:
                    cur.execute("INSERT INTO [ApartmentRentalDB].[dbo].[Interest] (UserId, ApartmentId) VALUES (" + str(userId) + ", " + str(apartmentId) + ");")
                    conn.commit()
                else:
                    return error_page(418, "User already exists in interest table")
            else:
                  return error_page(418, "User is not a tenant") 
        else:
            return error_page(418, "Tenant user or apartment does not exist")
        
        
        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] WHERE Id = SCOPE_IDENTITY()").fetchall()
        if len(results) > 0:
            for interest in results:
                response = (
                    {'Id': interest.Id,
                    'UserId': interest.UserId,
                    'ApartmentId': interest.ApartmentId}
                )
            return jsonify(response)
    else:
        return error_page(418, "User id, Apartment id can't be NULL")

@app.route('/api/update/interest', methods=['PUT'])
def updateInterest():
    data = ['Id', 'UserId', 'ApartmentId']

    for x in data:
        try: request.json[x]
        except KeyError: return error_page(418, x + " not set")

    if request.json['UserId'] != None and request.json['ApartmentId']:
        Id = request.json['Id']
        userId = request.json['UserId']
        apartmentId = request.json['ApartmentId']
            
        cur = conn.cursor()
        userResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(userId)).fetchall()
        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] WHERE Id= " + str(Id)).fetchall()
        interestResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] WHERE UserId = " + str(userId) + " AND NOT Id = " + str(Id)).fetchall()

        if len(results) > 0 and len(userResult) > 0:
            if userResult[0].Landlord == False:
                if len(interestResult) == 0:
                    cur.execute("UPDATE [ApartmentRentalDB].[dbo].[Interest] SET UserId= " + str(userId) + ", ApartmentId= " + str(apartmentId) + " WHERE Id= " + str(Id))
                    conn.commit()
                    results1 = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] WHERE Id= " + str(Id)).fetchall()
                    for interest in results1:
                        response = (
                            {'Id': interest.Id,
                            'UserId': interest.UserId,
                            'ApartmentId': interest.ApartmentId}
                        )
                    return jsonify(response)
                else:
                    return error_page(418, "User already exists in table")
            else:
                return error_page(418, "User is not a tenant")
        else:
            return error_page(418, "Could not find interest list")

    else:
        return error_page(418, "Not all fields are filled out buddy")

@app.route('/api/delete/interest/<Id>', methods=['DELETE'])
def  deleteInterest(Id):
    cur = conn.cursor()

    results1 = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Interest] WHERE Id =' + Id).fetchall()

    if len(results1) > 0:
        
        cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[Interest] WHERE Id = ' + Id)
        conn.commit()

        return "<h1>Deleted! wow!</h1>"
    else:
        return error_page(418, "Interest list not found")


#-------------------------------------------------------------------------------------------------------
#                                          END OF INTEREST SERVICE
#-------------------------------------------------------------------------------------------------------

@app.route('/api/read/rentals', methods=['GET'])
def getAllRentals():
    cur = conn.cursor()
    results = []
    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[RentalOffer];').fetchall()
        
    response = []

    for rental in results:
        response.append(
            {'Id': rental.Id,
            'LandlordId': rental.LandlordId,
            'ApartmentId': rental.ApartmentId,
            'UserId': rental.UserId}
        )
        
    return jsonify(response)

@app.route('/api/read/rental', methods=['GET'])
def getSpecificRental():
    cur = conn.cursor()
    to_filter = []
    if 'userid' in request.args:
        userId = (request.args['userid'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")
        to_filter.append("UserId = " + userId) 

    if 'landlordid' in request.args:
        landlordId = (request.args['landlordid'])
        if len(to_filter) >= 1:
            to_filter.append(" AND ")
        to_filter.append("LandlordId =" + landlordId)

    strFilter = "WHERE "
    for x in to_filter:
        strFilter += x

    if len(to_filter) > 0:
        results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[RentalOffer] ' + strFilter).fetchall()
        response = []

        if len(results) > 0:
            for rental in results:
                response.append(
                    {'Id': rental.Id,
                    'LandlordId': rental.LandlordId,
                    'ApartmentId': rental.ApartmentId,
                    'UserId': rental.UserId}
                )
            
            return jsonify(response)
        else:
            return error_page(418, "Rental offer not found")
    else:
        return error_page(418, "Need to use atleast one parameter")

@app.route('/api/create/rental', methods=['POST'])
def createRental():
    
    data = ['LandlordId', 'ApartmentId', 'UserId']

    for x in data:
        try: request.json[x]
        except KeyError: return error_page(418, x + " not set")

    if request.json['UserId'] != None and request.json['ApartmentId'] and request.json['LandlordId'] != None:
        userId = request.json['UserId']
        apartmentId = request.json['ApartmentId']
        landlordId = request.json['LandlordId']

        cur = conn.cursor()

        userResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(userId)).fetchall()
        landlordResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(landlordId)).fetchall()
        apartmentResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id = " + str(apartmentId)).fetchall()
        if len(apartmentResult) > 0:

            if len(userResult) > 0 and len(landlordResult) > 0:
                if userResult[0].Landlord == False and landlordResult[0].Landlord == True:
                    cur.execute("INSERT INTO [ApartmentRentalDB].[dbo].[RentalOffer] (LandlordId, ApartmentId, UserId) VALUES (" + str(landlordId) + ", " + str(apartmentId) + ", " + str(userId) + ");")
                    conn.commit()
                else:
                    return error_page(418, "Tenant is not a tenant or landlord is not a landlord")  
            else:
                return error_page(418, "Could not find user")
        else:
            return error_page(418, "Could not find apartment")
        
        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE Id = SCOPE_IDENTITY()").fetchall()
        if len(results) > 0:
            for rental in results:
                response = (
                    {'Id': rental.Id,
                    'LandlordId': rental.LandlordId,
                    'ApartmentId': rental.ApartmentId,
                    'UserId': rental.UserId}
                )
            return jsonify(response)
    else:
        return error_page(418, "User id, Apartment id and landlord id can't be NULL")

@app.route('/api/update/rental', methods=['PUT'])
def updateRental():
    data = ['Id', 'LandlordId', 'ApartmentId', 'UserId']

    for x in data:
        try: request.json[x]
        except KeyError: return error_page(418, x + " not set")

    if request.json['UserId'] != None and request.json['ApartmentId'] and request.json['LandlordId'] != None:
        Id = request.json['Id']
        userId = request.json['UserId']
        apartmentId = request.json['ApartmentId']
        landlordId = request.json['LandlordId']

            
        cur = conn.cursor()
        userResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(userId)).fetchall()
        landlordResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(landlordId)).fetchall()
        apartmentResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Apartment] WHERE Id = " + str(apartmentId)).fetchall()
        
        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE Id= " + str(Id)).fetchall()

        if len(results) > 0 and len(apartmentResult) > 0:
            
            if len(userResult) > 0 and len(landlordResult) > 0:
                if userResult[0].Landlord == False and landlordResult[0].Landlord == True:
                    cur.execute("UPDATE [ApartmentRentalDB].[dbo].[RentalOffer] SET LandlordId= " + str(landlordId) + ", ApartmentId= " + str(apartmentId) + ", UserId= " + str(userId) + " WHERE Id= " + str(Id))
                    conn.commit()
                    
                else:
                    return error_page(418, "Tenant is not a tenant or landlord is not a landlord")  
            else:
                return error_page(418, "Could not find user or apartment")

            results1 = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE Id= " + str(Id)).fetchall()
            for rental in results1:
                response = (
                    {'Id': rental.Id,
                    'LandlordId': rental.LandlordId,
                    'ApartmentId': rental.ApartmentId,
                    'UserId': rental.UserId}
                )
            
            return jsonify(response)
        else:
            return error_page(418, "Could not find rental offer or apartment")

    else:
        return error_page(418, "Not all fields are filled out buddy")

@app.route('/api/delete/rental/<Id>', methods=['DELETE'])
def  deleteRental(Id):
    cur = conn.cursor()

    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE Id =' + Id).fetchall()

    if len(results) > 0:
        
        cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[RentalOffer] WHERE Id = ' + Id)
        conn.commit()

        return "<h1>Deleted! wow!</h1>"
    else:
        return error_page(418, "Rental offer not found")


#-------------------------------------------------------------------------------------------------------
#                                          END OF RENTAL OFFER SERVICE
#-------------------------------------------------------------------------------------------------------

@app.route('/api/read/points', methods=['GET'])
def getAllPoints():
    cur = conn.cursor()
    results = []
    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Point];').fetchall()
        
    response = []

    for point in results:
        response.append(
            {'Id': point.Id,
            'UserId': point.UserId,
            'Points': point.Points}
        )
        
    return jsonify(response)

@app.route('/api/read/point/<Id>', methods=['GET'])
def getPointFromUser(Id):
    cur = conn.cursor()
    
    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Point] WHERE UserId = ' + Id).fetchall()

    if len(results) > 0:
        for point in results:
            response = (
                {'Id': point.Id,
                'UserId': point.UserId,
                'Points': point.Points}
            )
        
        return jsonify(response)
    else:
        return error_page(418, "User not found")


@app.route('/api/create/point', methods=['POST'])
def createPoint():
    
    data = ['UserId', 'Points']

    for x in data:
        try: request.json[x]
        except KeyError: return error_page(418, x + " not set")

    if request.json['UserId'] != None:
        userId = request.json['UserId']
        points = 0

        cur = conn.cursor()

        userResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(userId)).fetchall()
        pointResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Point] WHERE UserId = " + str(userId)).fetchall()
        
        if len(userResult) > 0 and len(userResult) > 0 and len(pointResult) < 1:
            
            if userResult[0].Landlord == False:
                cur.execute("INSERT INTO [ApartmentRentalDB].[dbo].[Point] (UserId, Points) VALUES (" + str(userId) + ", " + str(points) + ");")
                conn.commit()
        else:
            return error_page(418, "User does not exist or user already exists in point")
        
        
        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Point] WHERE Id = SCOPE_IDENTITY()").fetchall()
        if len(results) > 0:
            for point in results:
                response = (
                    {'Id': point.Id,
                    'UserId': point.UserId,
                    'Points': point.Points}
                )
            return jsonify(response)
    else:
        return error_page(418, "User id can't be NULL")

@app.route('/api/update/point', methods=['PUT'])
def updatePoint():
    data = ['Id', 'UserId', 'Points']

    for x in data:
        try: request.json[x]
        except KeyError: return error_page(418, x + " not set")

    if request.json['UserId'] != None and request.json['Points']:
        Id = request.json['Id']
        userId = request.json['UserId']
        points = request.json['Points']

            
        cur = conn.cursor()
        userResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[User] WHERE Id = " + str(userId)).fetchall()
        pointResult = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Point] WHERE UserId = " + str(userId) + " AND NOT Id = " + str(Id)).fetchall()
        results = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Point] WHERE Id= " + str(Id)).fetchall()
        print()
        if len(results) > 0 and len(userResult) > 0 and len(pointResult) == 0:
            if userResult[0].Landlord == False:
                cur.execute("UPDATE [ApartmentRentalDB].[dbo].[Point] SET UserId= " + str(userId) + ", Points = " + str(points) + " WHERE Id= " + str(Id))
                conn.commit()
                results1 = cur.execute("SELECT * FROM [ApartmentRentalDB].[dbo].[Point] WHERE Id= " + str(Id)).fetchall()
                
                for point in results1:
                    response = (
                        {'Id': point.Id,
                        'UserId': point.UserId,
                        'Points': point.Points}
                    )
                
                return jsonify(response)
        else:
            return error_page(418, "Could not find user or user already exists in point")

    else:
        return error_page(418, "Not all fields are filled out buddy")

@app.route('/api/delete/point/<Id>', methods=['DELETE'])
def  deletePoint(Id):
    cur = conn.cursor()

    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Point] WHERE Id =' + Id).fetchall()

    if len(results) > 0:
        
        cur.execute('DELETE FROM [ApartmentRentalDB].[dbo].[Point] WHERE Id = ' + Id)
        conn.commit()

        return "<h1>Deleted! wow!</h1>"
    else:
        return error_page(418, "Point not found")

def updatePointTime():

    cur = conn.cursor()

    results = cur.execute('SELECT * FROM [ApartmentRentalDB].[dbo].[Point]').fetchall()
    for user in results:
        print(user.Id)
        print(user.Points)

    for user in results:
        newPoints = user.Points + 5
        cur.execute('UPDATE [ApartmentRentalDB].[dbo].[Point] SET Points = ' + str(newPoints) + ' WHERE Id = ' + str(user.Id))

    cur.commit()

    return "<h1>Updated</h1>"


schedule.every().day.at("10:00").do(updatePointTime)

def startTimer():
    while(True):
        schedule.run_pending()
        time.sleep(1)


class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
        print("THREAD START BEEP BOOP")
        startTimer()
        print("THREAD DEAD")

thread1 = myThread(1, "Thread-1", 1)

thread1.start()

app.run()

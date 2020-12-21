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



    #metoder ATT GÖRA
    #CRUD för apartment
    #CRUD för interest list
    #CRUD för rental offer
    #CRUD för point
    #Funktion för att poäng skall uppdateras automatisk efter en viss tid
    #Filter funktion sortera efter price (range ex 300-2000), location och size



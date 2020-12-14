import flask
import mysql.connector

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    mydb = mysql.connector.connect(
        host="193.10.202.77",
        user="sa",
        password="TSB100sql"
    )
    print(mydb)
    return "<h1>snopp</h1>"

app.run()
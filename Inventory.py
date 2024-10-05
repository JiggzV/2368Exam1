import mysql.connector
from mysql.connector import Error

import flask
from flask import jsonify
from flask import request


#Setting the Application name
app = flask.Flask(__name__) #Sets up the application
app.config["DEBUG"] = True #Allow to show errors in browser

def create_con(hostname, username, userpw, dbname):
    connection = None
    try: 
        connection = mysql.connector.connect(
            host = hostname,
            user = username, 
            password = userpw,
            database= dbname
        )
        print('connection successful')
    except Error as e:
        print(f'the error {e} occured')
    return connection

conn = create_con('cis2368fall.c5yum806yt73.us-east-2.rds.amazonaws.com', 'admin', 'cis2368fallpass', 'cis2368falldb')
cursor = conn.cursor(dictionary=True)

#Creds.py and info needed to connect to MySQL DB

cursor.execute('''
CREATE TABLE IF NOT EXISTS INVENTORY(
id INT AUTO_INCREMENT,
name VARCHAR(60) NOT NULL,
quantity INT(50) NOT NULL,
price INT(50) NOT NULL)


);

''')

#Setting up the 'POST' Endpoint (We'll be using my code from HW2 to name and initialize endpoint)
@app.route('/api/additems', methods = ['POST'])
def add_item():
    request_data = request.get_json()  
    cursor = conn.cursor()
    newid = request_data['id']
    newname = request_data['name']
    newquantity = request_data['quantity']
    newprice = request_data['price']
    
    query = 'INSERT INTO INVENTORY( id, name, quantity, price) VALUES (%s, %s, %s, %s)' #SQL Query (almost the same as past codes)
    values = (newid, newname, newquantity, newprice)
    cursor.execute(query, values)
    conn.commit()
    return jsonify ({'Message: Item has been successfully added!', 200})



#Setting up my 'GET' Endpoint
@app.route('/api/currentinventory', methods = ['GET'])
def get_items():
    try:
        cursor = conn.cursor()
        query = 'SELECT * FROM INVENTORY'
        cursor.execute(query)
        result = cursor.fetchall(query)
        
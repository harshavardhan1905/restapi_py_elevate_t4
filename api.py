from flask import Flask,request, jsonify
import mysql.connector
# import mysql.connector

app = Flask(__name__)
db_config ={
    'host':'localhost',
    'user':'root',
    'password':'',
    'database':'elevatelabs'
}

#GET api creation
@app.route('/data', methods=['GET'])
def get_data():
    try:
        #connect to mysql
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) 

        #execute query
        cursor.execute("SELECT * from elevate_t4")
        #fetching rows
        rows = cursor.fetchall()

        #close connection
        cursor.close()
        conn.close()
        
        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"Error:": str(err)})
#POST api creation
@app.route("/post", methods=['POST'])
def post_data():
    try:
        #getting data from request body
        data = request.get_json()
        id = data.get('id')
        firstname = data.get('firstname')
        lastname = data.get('lastname')

        #connect to mysql 
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        #insert query
        if(id is not None and firstname is not None and lastname is not None):
            cursor.execute(
            "INSERT INTO elevate_t4(id, firstname, lastname) values(%s, %s, %s)", (id, firstname, lastname))
            conn.commit()

            cursor.close()
            conn.close()
        else:
            return "passing data with null values"
        return jsonify({"Message":"Data insert successfully!!.."}), 201
    except mysql.connector.Error as err:
        return jsonify({"Error": err}), 500



#running api
if __name__ == '__main__':
    app.run(debug=True)
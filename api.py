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

#api for updating data
@app.route("/update/<int:id>", methods=['PUT'])
def update_data(id):
    try:
        data = request.get_json()
        firstname = data.get('firstname')
        lastname = data.get('lastname')

        if not firstname or not lastname:
            return jsonify({"error":"Both first and lastnames are required"}), 400
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        #query to update
        cursor.execute("""UPDATE elevate_t4 
                        set firstname = %s, lastname = %s
                        where id = %s""",(firstname, lastname, id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message":"data updated successfully"})
    except mysql.connector.Error as err:
        return jsonify({"Error": str(err)})
@app.route("/delete/id/<int:id>", methods=['DELETE'])
def delete_data(id):
    try:
        # data = request.get_json()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # total = cursor.execute("select count(*) as total from elevate_t4")
        # if(total<=0):
        #     return "tables has 0 rows"
        cursor.execute("DELETE FROM elevate_t4 WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"Message":"Deleted data"})
    except mysql.connector.Error as err:
        return jsonify({"errors": str(err)})
#running api
if __name__ == '__main__':
    app.run(debug=True)
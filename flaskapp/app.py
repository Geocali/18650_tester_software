from flask import Flask, render_template, jsonify
import mysql.connector as mariadb

from flask_cors import CORS

app = Flask(__name__)

@app.route("/")
def main():
    #return render_template('battery_test.html')

    img = 'static/battery/Batteries-1379208.svg'
    return render_template('battery_test.html', img=img)


@app.route("/battery_measures", methods=['GET'])
def get_battery_measures():
    mariadb_connection = mariadb.connect(user='root', password='caramel', database='battery_schema')
    cursor = mariadb_connection.cursor()

    cursor.execute("SELECT slot_id, voltage, testing FROM battery_measures")
    data = []
    columns = tuple([d[0] for d in cursor.description])
    for row in cursor:
        data.append(dict(zip(columns, row)))
    mariadb_connection.close()
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run()

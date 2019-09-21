from flask import Flask, render_template, jsonify
import mysql.connector as mariadb
import pandas as pd

from flask_cors import CORS

app = Flask(__name__)


@app.route("/")
def main():
    #return render_template('battery_test.html')

    img = 'static/battery/Batteries-1379208.svg'
    return render_template('battery_test.html', img=img)


@app.route("/all_battery_measures", methods=['GET'])
def get_all_battery_measures():
    mariadb_connection = mariadb.connect(user='root', password='caramel', database='battery_schema')
    cursor = mariadb_connection.cursor()

    cursor.execute("SELECT * FROM measures")
    data = []
    columns = tuple([d[0] for d in cursor.description])
    for row in cursor:
        data.append(dict(zip(columns, row)))
    mariadb_connection.close()
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/last_battery_measures", methods=['GET'])
def get_last_battery_measures():
    mariadb_connection = mariadb.connect(user='root', password='caramel', database='battery_schema')
    cursor = mariadb_connection.cursor()

    cursor.execute("SELECT * FROM measures")
    data = []
    columns = tuple([d[0] for d in cursor.description])
    for row in cursor:
        data.append(dict(zip(columns, row)))
    mariadb_connection.close()
    df_data = pd.DataFrame(data)
    r_data = []
    for slot_id in df_data.slot_id.unique():
        df_slot = df_data[df_data.slot_id == slot_id]
        last_measure = df_slot[df_slot.time == df_slot.time.max()]
        r_data.append(last_measure.to_dict("records")[0])
    response = jsonify(r_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run()

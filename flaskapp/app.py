from flask import Flask, render_template, jsonify
import mysql.connector as mariadb
import pandas as pd
import numpy as np

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
    
    r_data = []
    for slot_id in [1, 2, 3, 4]:
        
        request_last_measure = "SELECT * FROM measures WHERE measures.time = (SELECT MAX(time) FROM measures WHERE measures.slot_id = " \
                               + str(float(slot_id)) \
                               + ") AND measures.slot_id = " \
                               + str(float(slot_id))
        last_measure = pd.read_sql_query(request_last_measure, mariadb_connection)

        request_times_last_session = "SELECT * FROM measures WHERE measures.testing_session = " \
                                     + str(last_measure.testing_session.values[0]) \
                                     + " AND measures.slot_id = " \
                                     + str(last_measure.slot_id.values[0]) \
                                     + " AND measures.testing = 1"
        data_testing = pd.read_sql_query(request_times_last_session, mariadb_connection)

        timediffs = (data_testing.time.diff() / np.timedelta64(1, 'h')).values[1:]
        voltages = data_testing.iloc[1:].voltage.values
        currents = voltages / 4  # R = 4 Ohm
        total_mah = (timediffs * currents).sum()

        last_measure['total_ah'] = total_mah

        r_data.append(last_measure.to_dict("records")[0])
    mariadb_connection.close()
    response = jsonify(r_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run()

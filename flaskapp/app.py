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


@app.route("/last_battery_measures", methods=['GET'])
def get_last_battery_measures():
    df = pd.read_csv("output/measures.csv")
    
    r_data = []
    for slot_id in [1, 2, 3, 4]:

        df_measures_slot = df[df.slot_id == slot_id]
        df_last_measure_slot = df_measures_slot[df_measures_slot.time == df_measures_slot.time.max()]
        df_last_measure_slot['time'] = pd.to_datetime(df_last_measure_slot.time)

        timediffs = (df_last_measure_slot.time.diff() / np.timedelta64(1, 'h')).values[1:]
        voltages = df_last_measure_slot.iloc[1:].voltage.values
        currents = voltages / 4  # R = 4 Ohm
        total_mah = (timediffs * currents).sum()

        df_last_measure_slot['total_ah'] = total_mah

        r_data.append(df_last_measure_slot.to_dict("records")[0])
    
    response = jsonify(r_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

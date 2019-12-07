from flask import Flask, render_template, jsonify
import mysql.connector as mariadb
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from flask_cors import CORS

app = Flask(__name__)
csv_file = "output/measures.csv"


def create_plot():

    df = pd.read_csv(csv_file)

    df_slot1 = df[df.slot_id == 1]
    df1 = df_slot1[df_slot1.testing_session == df_slot1.testing_session.max()]
    df_slot2 = df[df.slot_id == 2]
    df2 = df_slot2[df_slot2.testing_session == df_slot2.testing_session.max()]
    df_slot3 = df[df.slot_id == 3]
    df3 = df_slot3[df_slot3.testing_session == df_slot3.testing_session.max()]
    df_slot4 = df[df.slot_id == 4]
    df4 = df_slot4[df_slot4.testing_session == df_slot4.testing_session.max()]

    fig = make_subplots(rows=2, cols=2, subplot_titles=("Slot 1", "Slot 2", "Slot 3", "Slot 4"))
    fig.add_trace(
        go.Scatter(
            x=df1['time'], # assign x as the dataframe column 'x'
            y=df1['voltage']
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df[df.slot_id == 2]['time'], # assign x as the dataframe column 'x'
            y=df[df.slot_id == 2]['voltage']
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=df[df.slot_id == 3]['time'], # assign x as the dataframe column 'x'
            y=df[df.slot_id == 3]['voltage']
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df[df.slot_id == 4]['time'], # assign x as the dataframe column 'x'
            y=df[df.slot_id == 4]['voltage']
        ),
        row=2, col=2
    )
    fig.update_layout(height=800, width=1000, title_text="Batteries")

    fig['layout'].update(
        annotations=[
        dict(
            x=df1.time.values[-1], y=df1.voltage.values[-1], # annotation point
            xref='x1', 
            yref='y1',
            text=str(df1.spent_mah.values[-1]) + 'mAh',
            showarrow=True,
            arrowhead=7,
            ax=10,
            ay=70
        ),
        dict(
            x=df2.time.values[-1], y=df2.voltage.values[-1], # annotation point
            xref='x2', 
            yref='y2',
            text=str(df2.spent_mah.values[-1]) + 'mAh',
            showarrow=True,
            arrowhead=7,
            ax=10,
            ay=70
        ),
        dict(
            x=df3.time.values[-1], y=df3.voltage.values[-1], # annotation point
            xref='x3', 
            yref='y3',
            text=str(df3.spent_mah.values[-1]) + 'mAh',
            showarrow=True,
            arrowhead=7,
            ax=10,
            ay=70
        ),
        dict(
            x=df4.time.values[-1], y=df4.voltage.values[-1], # annotation point
            xref='x4', 
            yref='y4',
            text=str(df4.spent_mah.values[-1]) + 'mAh',
            showarrow=True,
            arrowhead=7,
            ax=10,
            ay=70
        ),
    ])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route("/")
def index():

    plot = create_plot()
    return render_template('index.html', plot=plot)


@app.route("/last_battery_measures", methods=['GET'])
def get_last_battery_measures():
    df = pd.read_csv(csv_file)
    
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

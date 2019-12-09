from flask import Flask, render_template, jsonify
import mysql.connector as mariadb
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os

from flask_cors import CORS

app = Flask(__name__)
csv_file = "output/measures.csv"


def create_plot():

    if not os.path.isfile(csv_file):
        df = pd.DataFrame(columns=['time', 'slot_id', 'voltage', 'testing', 'testing_session', 'spent_mah'])
    else:
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
    
    # ========== slot 1 ============
    fig.add_trace(
        go.Scatter(
            x=df1['time'], # assign x as the dataframe column 'x'
            y=df1['voltage'],
            name='voltage slot 1',
            line=dict(color='royalblue', width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=pd.concat([df1.head(1), df1.tail(1)])['time'], # assign x as the dataframe column 'x'
            y=[3, 3],
            mode='lines',
            name='end test voltage',
            line=dict(color='black', width=2)
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=pd.concat([df1.head(1), df1.tail(1)])['time'], # assign x as the dataframe column 'x'
            y=[4, 4],
            mode='lines',
            name='start test voltage',
            line=dict(color='black', width=2)
        ),
        row=1, col=1
    )
    if df1[df1.testing == True].shape[0] > 0:
        t_start_test = df1[df1.testing == True].iloc[0].time
        t_end_test = df1[df1.testing == True].iloc[-1].time
        fig.add_shape(
            # filled Rectangle
            go.layout.Shape(
                type="rect",
                x0=t_start_test,
                y0=3,
                x1=t_end_test,
                y1=4,
                line=dict(
                    color="RoyalBlue",
                    width=2,
                ),
                fillcolor="LightSkyBlue",
                            opacity=0.5,
                layer="below",
                line_width=0,
            ),
            row=1, col=1
            )
        fig.update_shapes(dict(xref='x1', yref='y1'))

    # =========== slot 2 ==============
    fig.add_trace(
        go.Scatter(
            x=df2['time'], # assign x as the dataframe column 'x'
            y=df2['voltage'],
            name="voltage slot 2",
            line=dict(color='royalblue', width=2)
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=pd.concat([df2.head(1), df2.tail(1)])['time'], # assign x as the dataframe column 'x'
            y=[3, 3],
            mode='lines',
            name='end test voltage',
            line=dict(color='black', width=2)
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=pd.concat([df2.head(1), df2.tail(1)])['time'], # assign x as the dataframe column 'x'
            y=[4, 4],
            mode='lines',
            name='start test voltage',
            line=dict(color='black', width=2)
        ),
        row=1, col=2
    )
    if df2[df2.testing == True].shape[0] > 0:
        t_start_test = df2[df2.testing == True].iloc[0].time
        t_end_test = df2[df2.testing == True].iloc[-1].time
        fig.add_shape(
            # filled Rectangle
            go.layout.Shape(
                type="rect",
                x0=t_start_test,
                y0=3,
                x1=t_end_test,
                y1=4,
                line=dict(
                    color="RoyalBlue",
                    width=2,
                ),
                fillcolor="LightSkyBlue",
                            opacity=0.5,
                layer="below",
                line_width=0,
            ),
            row=1, col=2
            )
        fig.update_shapes(dict(xref='x2', yref='y2'))

    # ========= slot 3 =========
    fig.add_trace(
        go.Scatter(
            x=df3['time'], # assign x as the dataframe column 'x'
            y=df3['voltage'],
            name="voltage slot 3",
            line=dict(color='royalblue', width=2)
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=pd.concat([df3.head(1), df3.tail(1)])['time'], # assign x as the dataframe column 'x'
            y=[3, 3],
            mode='lines',
            name='end test voltage',
            line=dict(color='black', width=2)
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=pd.concat([df3.head(1), df3.tail(1)])['time'], # assign x as the dataframe column 'x'
            y=[4, 4],
            mode='lines',
            name='start test voltage',
            line=dict(color='black', width=2)
        ),
        row=2, col=1
    )
    if df3[df3.testing == True].shape[0] > 0:
        t_start_test = df3[df3.testing == True].iloc[0].time
        t_end_test = df3[df3.testing == True].iloc[-1].time
        fig.add_shape(
            # filled Rectangle
            go.layout.Shape(
                type="rect",
                x0=t_start_test,
                y0=3,
                x1=t_end_test,
                y1=4,
                line=dict(
                    color="RoyalBlue",
                    width=2,
                ),
                fillcolor="LightSkyBlue",
                            opacity=0.5,
                layer="below",
                line_width=0,
            ),
            row=2, col=1
            )
        fig.update_shapes(dict(xref='x3', yref='y3'))

    # ========== slot 4 ===========
    fig.add_trace(
        go.Scatter(
            x=df4['time'], # assign x as the dataframe column 'x'
            y=df4['voltage'],
            name="voltage slot 4",
            line=dict(color='royalblue', width=2)
        ),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=pd.concat([df4.head(1), df4.tail(1)])['time'], # assign x as the dataframe column 'x'
            y=[3, 3],
            mode='lines',
            name='end test voltage',
            line=dict(color='black', width=2)
        ),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=pd.concat([df4.head(1), df4.tail(1)])['time'], # assign x as the dataframe column 'x'
            y=[4, 4],
            mode='lines',
            name='start test voltage',
            line=dict(color='black', width=2)
        ),
        row=2, col=2
    )
    if df4[df4.testing == True].shape[0] > 0:
        t_start_test = df4[df4.testing == True].iloc[0].time
        t_end_test = df4[df4.testing == True].iloc[-1].time
        fig.add_shape(
            # filled Rectangle
            go.layout.Shape(
                type="rect",
                x0=t_start_test,
                y0=3,
                x1=t_end_test,
                y1=4,
                line=dict(
                    color="RoyalBlue",
                    width=2,
                ),
                fillcolor="LightSkyBlue",
                            opacity=0.5,
                layer="below",
                line_width=0,
            ),
            row=2, col=2
            )
        fig.update_shapes(dict(xref='x4', yref='y4'))


    fig.update_layout(height=800, width=1000, title_text="Batteries", showlegend=False)

    if df1.shape[0] == 0:
        dict1 = {}
    else:
        dict1 = dict(
            x=df1.tail(1).time.values[0], y=df1.tail(1).voltage.values[0], # annotation point
            xref='x1', 
            yref='y1',
            text=str(round(df1.spent_mah.max(), 3)) + 'mAh',
            showarrow=True,
            arrowhead=7,
            ax=10,
            ay=70
        )
    if df2.shape[0] == 0:
        dict2 = {}
    else:
        dict2 = dict(
            x=df2.tail(1).time.values[0], y=df2.tail(1).voltage.values[0], # annotation point
            xref='x2', 
            yref='y2',
            text=str(round(df2.spent_mah.max(), 3)) + 'mAh',
            showarrow=True,
            arrowhead=7,
            ax=10,
            ay=70
        )
    if df3.shape[0] == 0:
        dict3 = {}
    else:
        dict3 = dict(
            x=df3.tail(1).time.values[0], y=df3.tail(1).voltage.values[0], # annotation point
            xref='x3', 
            yref='y3',
            text=str(round(df3.spent_mah.max(), 3)) + 'mAh',
            showarrow=True,
            arrowhead=7,
            ax=10,
            ay=70
        )
    if df4.shape[0] == 0:
        dict4 = {}
    else:
        dict4 = dict(
            x=df4.tail(1).time.values[0], y=df4.tail(1).voltage.values[0], # annotation point
            xref='x4', 
            yref='y4',
            text=str(round(df4.spent_mah.max(), 3)) + 'mAh',
            showarrow=True,
            arrowhead=7,
            ax=10,
            ay=70
        )

    fig['layout'].update(
        annotations=[
        dict1,
        dict2,
        dict3,
        dict4
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

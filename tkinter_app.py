import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import Canvas
from tkinter import messagebox as msg

import numpy as np
import pandas as pd
import time

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.pyplot as plt

import tester


class TesterOutline(tk.Tk):

    def __init__(self):
        # Inherit from tk.Tk
        super().__init__()

        # Title and size of the window
        self.title('18650 battery tester')
        self.geometry('600x400')

        # Create the drop down menus
        self.menu = tk.Menu(self,bg='lightgrey',fg='black')

        self.file_menu = tk.Menu(self.menu,tearoff=0,bg='lightgrey',fg='black')
        self.file_menu.add_command(label='Add Project',command=self.unfinished)
        self.file_menu.add_command(label='Quit',command=self.quit)

        self.menu.add_cascade(label='File',menu=self.file_menu)

        self.config(menu=self.menu)

        # Create the tabs (Graph, File Explorer, etc.)
        self.notebook = Notebook(self)

        graph_tab = tk.Frame(self.notebook)
        file_explorer_tab = tk.Frame(self.notebook)

        # Sets the Graph Tab as a Canvas where figures, images, etc. can be added
        self.graph_tab = tk.Canvas(graph_tab)
        self.graph_tab.pack(side=tk.TOP, expand=1)

        # Sets the file explorer tab as a text box (change later)
        self.file_explorer_tab = tk.Text(file_explorer_tab,bg='white',fg='black')
        self.file_explorer_tab.pack(side=tk.TOP, expand=1)

        # Add the tabs to the GUI
        self.notebook.add(graph_tab, text='Graph')
        self.notebook.add(file_explorer_tab, text='Files')

        self.notebook.pack(fill=tk.BOTH, expand=1)

        # Add the graph to the graph tab
        self.fig = Figure()
        graph = FigureCanvasTkAgg(self.fig,self.graph_tab)
        graph.get_tk_widget().pack(side='top',fill='both',expand=True)
        MainGraph(self.fig)

    def quit(self):
        '''
        Quit the program
        '''
        self.destroy()

    def unfinished(self):
        '''
        Messagebox for unfinished items
        '''
        msg.showinfo('Unfinished','This feature has not been finished')


class MainGraph():

    def __init__(self,fig):
        self.fig = fig

        self.l, self.axes = plt.subplots(2, 2)

        df_measures = tester.main_function()

        df_values = df_measures[df_measures.slot_id == 1]
        x = (pd.to_datetime(df_values.time) - pd.to_datetime(df_values.time.iloc[0])).astype('timedelta64[m]').values[1:]
        y = df_values.voltage.values[1:]
        self.axes[0][0].plot(x, y)

        df_values = df_measures[df_measures.slot_id == 2]
        x = (pd.to_datetime(df_values.time) - pd.to_datetime(df_values.time.iloc[0])).astype('timedelta64[m]').values[1:]
        y = df_values.voltage.values[1:]
        self.axes[1][0].plot(x, y)

        time.sleep(1)

        df_measures = tester.main_function()

        df_values = df_measures[df_measures.slot_id == 1]
        x = (pd.to_datetime(df_values.time) - pd.to_datetime(df_values.time.iloc[0])).astype('timedelta64[m]').values[1:]
        y = df_values.voltage.values[1:]
        self.axes[0][0].plot(x, y)

        df_values = df_measures[df_measures.slot_id == 2]
        x = (pd.to_datetime(df_values.time) - pd.to_datetime(df_values.time.iloc[0])).astype('timedelta64[m]').values[1:]
        y = df_values.voltage.values[1:]
        self.axes[1][0].plot(x, y)



        plt.show()


        # df_measures = tester.main_function()
        # for slot_id in range(1, 5):
        #     df_values = df_measures[df_measures.slot_id == slot_id]
        #     self.l, = self.create_plot(df_values, slot_id)

        # i = 0
        # while i < 100:
        #     df_measures = tester.main_function()
        #     for slot_id in range(1, 5):
                
        #     time.sleep(1)
        #     i += 1

        # slot_id = 1
        # df_values = pd.read_csv("output/2019-12-09 151236_1_3_1302mAh.csv")
        # self.l, = self.create_plot(df_values, slot_id)

        # slot_id = 2
        # df_values = pd.read_csv("output/2019-12-09 152422_2_5_1510mAh.csv")
        # self.l, = self.create_plot(df_values, slot_id)

        # slot_id = 3
        # df_values = pd.read_csv("output/2019-12-09 155111_4_4_1935mAh.csv")
        # self.l, = self.create_plot(df_values, slot_id)

        # slot_id = 4
        # df_values = pd.read_csv("output/2019-12-09 160424_3_4_2153mAh.csv")
        # self.l, = self.create_plot(df_values, slot_id)


    def create_plot(self, df_measures):

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(2, 2)

        # Set up figure with centered axes and grid
        self.ax = self.fig.add_subplot(2, 2, slot_id)
        
        self.ax.set_ylim(2.8,4.3)
        self.ax.grid(color='lightgray',linestyle='--')

        # create time into minutes since beginning of test
        x = (pd.to_datetime(df_values.time) - pd.to_datetime(df_values.time.iloc[0])).astype('timedelta64[m]')
        y = df_values.voltage.values
        return self.ax.plot(x, y, 'k')


#----------------------------------------------------------

if __name__ == '__main__':
    tester_gui = TesterOutline()
    tester_gui.mainloop()

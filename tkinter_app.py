import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import Canvas
from tkinter import messagebox as msg

import numpy as np
import pandas as pd
import time
import os

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
        
        self.l, self.axes = plt.subplots(2, 2)
        self.create_plot()
        self.update_plot(graph)

    def create_plot(self):
        csv_file = 'output/measures.csv'
        if os.path.exists(csv_file):
            os.remove(csv_file)
            
        self.axes = []
        for slot_id in range(1, 5):
            self.axes.append(self.fig.add_subplot(2, 2, slot_id))
            x = [0]
            y = [3.5]
            curve, = self.axes[slot_id - 1].plot(x, y)

    def update_plot(self, graph):

        df_measures = tester.main_function()
        # TODO: plot curve only if the battery of the slot is currently testing
        for slot_id in range(1, 5):
            df_values = df_measures[df_measures.slot_id == slot_id]
            self.axes[slot_id - 1].clear()
            if df_values.iloc[-1].testing == 1:
                x = (pd.to_datetime(df_values.time) - pd.to_datetime(df_values.time.iloc[0])).astype('timedelta64[s]').values[1:]
                y = df_values.voltage.values[1:]
                curve, = self.axes[slot_id - 1].plot(x, y)
            else:
                left = 0.2
                bottom = 0.5
                self.axes[slot_id - 1].text(
                    left, 
                    bottom, 
                    'Waiting for battery',
                    horizontalalignment='left',
                    verticalalignment='top',
                    transform=self.axes[slot_id - 1].transAxes
                    )

        graph.draw()
        graph.flush_events() # flush the GUI events
        # call this function again in the future
        self.after(10000, self.update_plot(graph))
        

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


if __name__ == '__main__':
    tester_gui = TesterOutline()
    tester_gui.mainloop()

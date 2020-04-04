import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import Canvas
from tkinter import messagebox as msg

import numpy as np
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider, Button, RadioButtons

#----------------------------------------------------------

class TesterOutline(tk.Tk):

    #------------------------------------------------------
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

    #------------------------------------------------------
    def quit(self):
        '''
        Quit the program
        '''
        self.destroy()

    #------------------------------------------------------
    def unfinished(self):
        '''
        Messagebox for unfinished items
        '''
        msg.showinfo('Unfinished','This feature has not been finished')

    #------------------------------------------------------
    def random_graph(self):
        x = list(range(0,10))
        y = [i**3 for i in x]

        fig = Figure()
        axes = fig.add_subplot(111)
        axes.plot(x,y,label=r'$x^3$')
        axes.legend()

        return fig

#----------------------------------------------------------

class MainGraph():

    #------------------------------------------------------
    def __init__(self,fig):
        self.fig = fig

        i = 1
        df_values = pd.read_csv("output/2019-12-09 151236_1_3_1302mAh.csv")
        self.l, = self.create_plot(df_values, i)

        i = 2
        df_values = pd.read_csv("output/2019-12-09 152422_2_5_1510mAh.csv")
        self.l, = self.create_plot(df_values, i)

        i = 3
        df_values = pd.read_csv("output/2019-12-09 155111_4_4_1935mAh.csv")
        self.l, = self.create_plot(df_values, i)

        i = 4
        df_values = pd.read_csv("output/2019-12-09 160424_3_4_2153mAh.csv")
        self.l, = self.create_plot(df_values, i)


    def create_plot(self, df_values, i):

        # Set up figure with centered axes and grid
        self.ax = self.fig.add_subplot(2, 2, i)
        
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

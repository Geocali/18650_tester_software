import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import Canvas
from tkinter import messagebox as msg

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.widgets import Slider, Button, RadioButtons

#----------------------------------------------------------

class LukeOutline(tk.Tk):

    #------------------------------------------------------
    def __init__(self):
        # Inherit from tk.Tk
        super().__init__()

        # Title and size of the window
        self.title('Luke Outline')
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
        EllipseSlider(self.fig)

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

class EllipseSlider():

    #------------------------------------------------------
    def __init__(self,fig):
        self.fig = fig

        # Initial values
        self.u = 0.     #x-position of the center
        self.v = 0.     #y-position of the center
        self.a = 2.     #radius on the x-axis
        self.b = 1.5    #radius on the y-axis

        # Points to plot against
        self.t = np.linspace(0, 2*np.pi, 100)

        # Set up figure with centered axes and grid
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect(aspect='equal')
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.set_xlim(-2,2)
        self.ax.set_ylim(-2,2)
        self.ax.grid(color='lightgray',linestyle='--')

        # Initial plot
        self.l, = self.ax.plot(self.u+self.a*np.cos(self.t),
            self.v+self.b*np.sin(self.t),'k')

        # Slider setup
        self.axcolor = 'lightgoldenrodyellow'
        self.axb = self.fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=self.axcolor)
        self.axa = self.fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=self.axcolor)

        self.sb = Slider(self.axb, 'Y Radius', 0.1, 2.0, valinit=self.b)
        self.sa = Slider(self.axa, 'X Radius', 0.1, 2.0, valinit=self.a)

        # Call update as slider is changed
        self.sb.on_changed(self.update)
        self.sa.on_changed(self.update)

        # Reset if reset button is pushed
        self.resetax = self.fig.add_axes([0.8,0.025,0.1,0.04])
        self.button = Button(self.resetax, 'Reset', color=self.axcolor, hovercolor='0.975')

        self.button.on_clicked(self.reset)

        # Color button setup
        self.rax = self.fig.add_axes([0.025, 0.5, 0.15, 0.15], facecolor=self.axcolor)
        self.radio = RadioButtons(self.rax, ('red', 'blue', 'green'), active=0)

        self.radio.on_clicked(self.colorfunc)

    #------------------------------------------------------

    def update(self, val):
        '''
        Updates the plot as sliders are moved
        '''
        self.a = self.sa.val
        self.b = self.sb.val
        self.l.set_xdata(self.u+self.a*np.cos(self.t))
        self.l.set_ydata(self.u+self.b*np.sin(self.t))

    #------------------------------------------------------

    def reset(self, event):
        '''
        Resets everything if reset button clicked
        '''
        self.sb.reset()
        self.sa.reset()

    #------------------------------------------------------

    def colorfunc(self, label):
        '''
        Changes color of the plot when button clicked
        '''
        self.l.set_color(label)
        self.fig.canvas.draw_idle()

#----------------------------------------------------------

if __name__ == '__main__':
    luke_gui = LukeOutline()
    luke_gui.mainloop()

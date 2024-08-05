import tkinter as tk
from tkinter import ttk
import pandas as pd


class Application(tk.Tk):

    def __init__(self, width, height):
        super().__init__()
        self.title("Inventory Management")
        self.geometry(f'{width}x{height}')
        Menu(self)
        FilterFrame(self, "Inventory.csv")
        self.mainloop()


class Menu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        settings_menu = tk.Menu(self, tearoff=False)  # contains resolution, layout, change database,etc
        settings_menu.add_command(label="Resolution")
        settings_menu.add_command(label="Layout")
        settings_menu.add_command(label="Change Database")
        self.add_cascade(label="Settings", menu=settings_menu)
        #Help Menu#
        help_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Controls")
        help_menu.add_separator()
        help_menu.add_command(label="Mangament System")
        parent.configure(menu=self)


class FilterFrame(tk.Frame):
    def __init__(self, parent, dataframe):
        super().__init__(parent)
        # Frame
        self.configure(width = 300, height = 400, borderwidth = 10)
        self.dataframe = pd.read_csv(dataframe)
        self.pack_propagate(False)
        self.pack(side='top', fill='both')
        self.createDropdown()
        self.create_table()
        #Dropdown Widgets
    def createDropdown(self):
        # Label for the dropbox for finding keywords
        filter_label_Manufacture = tk.Label(self, text="Manufacture", font=("Helvetica", 12))
        filter_label_Manufacture.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
        filter_label_WidthSize = tk.Label(self, text="Width Size", font=("Helvetica", 12))
        filter_label_WidthSize.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
        filter_label_IDNum = tk.Label(self, text="ID #", font=("Helvetica", 12))
        filter_label_IDNum.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
        choices_Manufacture = ['', 'Shanghai', 'Fujikura', 'SuperPower']
        self.branch1_dropdown = ttk.Combobox(self, values=choices_Manufacture, width=11)
        self.branch1_dropdown.pack(anchor=tk.W, padx=0)

        choices_OpCom = ['', '<', '>', '=', '\u2265', '\u2264']
        self.branch2_dropdown = ttk.Combobox(self, values=choices_OpCom, width=1)
        self.branch2_dropdown.pack(anchor=tk.W)

        self.branch3_dropdown = ttk.Entry(self, width=3)
        self.branch3_dropdown.pack(anchor=tk.E)

        self.branch4_dropdown = ttk.Entry(self, width=10)
        self.branch4_dropdown.pack(anchor=tk.W)

        #Button Widget
        filter_button = ttk.Button(self, text='Filter', command=lambda: self.filter())
        filter_button.pack()

        #Grid
        #Colums
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        #Rows
        self.rowconfigure(0, weight=1)
        #Placement for the widgets in the grid
        filter_label_Manufacture.grid(row=0, column=0, sticky='w')
        filter_label_WidthSize.grid(row=0, column=1, sticky='W', padx=40)
        filter_label_IDNum.grid(row=0, column=2, sticky='W')
        #Dropdown widgets placements
        self.branch1_dropdown.grid(row=0, column=0, sticky='e')
        self.branch2_dropdown.grid(row=0, column=1, sticky='e', padx=130)
        self.branch3_dropdown.grid(row=0, column=1, sticky='e', padx=160)
        self.branch4_dropdown.grid(row=0, column=2, sticky='w', padx=55)
        filter_button.grid(row=0, column=4)

    def refresh(self, table):
        for row in table.get_children():
            table.delete(row)
    def create_table(self):
        self.table = ttk.Treeview(master = self)
        self.table.configure(columns=tuple(self.dataframe.columns), show="headings")
        for column in tuple(self.dataframe.columns):
            self.table.heading(column, text=column)
            self.table.column(column, anchor=tk.CENTER)
        for rows in self.dataframe.itertuples(index=False, name=None):
            self.table.insert(parent='', index=tk.END, values=tuple(rows))
        self.table.grid(row = 1, column = 0,pady = 20,ipady = 80, columnspan = 5, sticky = "swse",)

    def filter(self):
        newdataframe = self.dataframe
        columns = self.returnfilters()
        print(columns)
        for index, i in enumerate(columns):
            if i != '':
                try:
                    newdataframe = newdataframe.where(newdataframe[self.dataframe.columns[index]] == i)
                    newdataframe = newdataframe.dropna()
                except KeyError:
                    print("No data found index: " + str(index) + ", filter: " + i)
        self.refresh(self.table)
        for rows in newdataframe.itertuples(index=False):
            self.table.insert(parent='', index=tk.END, values=tuple(rows))
    def returnfilters(self):
        return [self.branch1_dropdown.get(), self.branch3_dropdown.get(), self.branch4_dropdown.get()]


Application("800", "500")

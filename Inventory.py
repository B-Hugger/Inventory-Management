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
        #Help Menu
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
        self.parent = parent
        #self.configure(width=300, height=400, borderwidth=10)
        #self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(1, weight=1)
        self.dataframe = pd.read_csv(dataframe)
        self.pack_propagate(False)
        self.pack( fill='both', expand = True)
        self.createDropdown()
        self.create_table()
        PopUpMenu(table = self.table, parent = parent)
    def createDropdown(self):
        #Dropdown Widgets
        manufacture_frame = tk.Frame(master= self)
        width_frame = tk.Frame(master=self)
        id_frame = tk.Frame(master=self)

        # Grid
        # Colums
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(2, weight=1)
        # self.columnconfigure(3, weight=1)
        # # Rows
        # self.rowconfigure(0, weight=3)

        manufacture_frame.grid(row=0, column=0)
        width_frame.grid(row=0, column=1)
        id_frame.grid(row=0, column=2)

        # Label for the dropbox for finding keywords
        filter_label_manufacture = tk.Label(manufacture_frame, text="Manufacture", font=("Helvetica", 12))
        filter_label_manufacture.pack(side="left", anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
        filter_label_widthsize = tk.Label(width_frame, text="Width Size", font=("Helvetica", 12))
        filter_label_widthsize.pack(side="left", anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
        filter_label_IDNum = tk.Label(id_frame, text="ID #", font=("Helvetica", 12))
        filter_label_IDNum.pack(side="left", anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
        choices_manufacture = ['', 'Shanghai', 'Fujikura', 'SuperPower']
        self.branch1_dropdown = DropDown(parent=manufacture_frame, column="Manufacturer",
                                         selections=choices_manufacture, width=11)

        self.branch1_dropdown.pack(anchor=tk.W, padx=0)
        choices_OpCom = ['', '<', '>', '=', '\u2265', '\u2264']
        self.branch2_dropdown = DropDown(parent=width_frame, column=None, selections=choices_OpCom, width=1)
        self.branch2_dropdown.pack(side="left", anchor=tk.W)

        self.branch3_dropdown = Entry(parent=width_frame, column="Size", width=3)
        self.branch3_dropdown.pack(side="left", anchor=tk.E)

        self.branch4_dropdown = Entry(parent=id_frame, column="Identification", width=10)
        self.branch4_dropdown.pack(side="left", anchor=tk.W)

        # Button Widget
        filter_button = ttk.Button(self, text='Filter', command=lambda: self.filter())
        filter_button.grid(row=0, column=3)

    def refresh(self, table):
        for row in table.get_children():
            table.delete(row)

    def create_table(self):
        #Table creation
        table_frame = tk.Frame(master = self)

        table_frame.grid(row = 1, column = 0, pady=20, ipady=80,columnspan=5,rowspan = 3, sticky="nsew" )
        self.table = ttk.Treeview(master= table_frame)
        self.table.configure(columns=tuple(self.dataframe.columns), show="headings")
        self.table.pack(fill=tk.BOTH, expand=True)
        #Table item fill
        for column in tuple(self.dataframe.columns):
            self.table.heading(column, text=column)
            self.table.column(column, anchor=tk.CENTER)
        for rows in self.dataframe.itertuples(index=False, name=None):
            self.table.insert(parent='', index=tk.END, values=tuple(rows))
        #Controls for table
        scrollbar = ttk.Scrollbar(self.table, orient=tk.VERTICAL, command = self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #Info display for table
        self.text = tk.StringVar()
        self.text.set("Total Items: " + str(len(self.table.get_children())))
        item_amount = tk.Label(master= table_frame, textvariable=self.text)
        item_amount.pack(side="left")
    def filter(self):
        newdataframe = self.dataframe
        columns = self.returnfilters()
        dictionary = {'<': '<', '>': '>', '=': "==", '\u2265': '>=', '\u2264': '<='}
        flag = False
        print(columns[0].get(), columns[1].get(), columns[2].get(), columns[3].get())
        for index, entry in enumerate(columns):
            if entry.get() != '':
                try:
                    if entry.get() in dictionary.keys() and columns[2].get() != '':
                        print(dictionary[entry.get()])
                        newdataframe = newdataframe.query(
                            f"{columns[2].column} {dictionary[entry.get()]} {columns[2].get()}")
                        flag = True
                    elif flag is True:
                        flag = False
                        continue
                    else:
                        newdataframe = newdataframe.where(newdataframe[entry.column] == entry.get())
                        newdataframe = newdataframe.dropna()
                except KeyError:
                    print("invalid key: " + ", filter: " + entry.get())
        self.refresh(self.table)
        for rows in newdataframe.itertuples(index=False):
            self.table.insert(parent='', index=tk.END, values=tuple(rows))
        self.text.set("Total Items: " + str(len(self.table.get_children())))



    def returnfilters(self):
        return [self.branch1_dropdown, self.branch2_dropdown, self.branch3_dropdown, self.branch4_dropdown]


class DropDown(ttk.Combobox):
    def __init__(self, parent, column, width, selections):
        super().__init__(master=parent, width=width, values=selections)
        self.selections = selections
        self.column = column


class Entry(tk.Entry):
    def __init__(self, parent, column, width):
        super().__init__(master=parent, width=width)
        self.column = column
#class PopupWindow()
class PopUpMenu(tk.Menu):
    def __init__(self, table, parent):
        super().__init__(parent)
        self.configure(tearoff=False)
        self.add_command(label="Add", command=self.filler)
        self.add_command(label="Delete", command=self.filler)
        self.table = table
        self.table.bind('<Button-3>',self.popup)
    def filler(self):
        print("pressed")
    def popup(self, event):
        # select row under mouse
        iid = self.table.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.table.selection_set(iid)
            self.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass


Application("800", "500")

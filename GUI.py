
import tkinter as tk
from tkinter import ttk
import pandas as pd


def refresh(table):
    for row in table.get_children():
        table.delete(row)

def filter(dataframe,table,columns = None, filter = None):
    newdataframe = dataframe
    for index, i in enumerate(filter):
        if i != '':
            try:
                newdataframe = newdataframe.where(newdataframe[dataframe.columns[index]] == i)
                newdataframe = newdataframe.dropna()

            except KeyError:
                print("No data found index: " + str(index) + ", filter: " + i)
    refresh(table)
    for rows in newdataframe.itertuples(index = False):
        table.insert(parent = '', index = tk.END, values = tuple(rows))

# Create the main application window
window = tk.Tk()
window.title("Inventory")  # Add a title to the window
window.geometry("800x500")  # Set the window size

#Menu

menu = tk.Menu(window)

    #Sub Menu
        ##Setttings Menu#
settings_menu = tk.Menu(menu,tearoff = False) # contains resolution, layout, change database,etc
settings_menu.add_command(label="Resolution")
settings_menu.add_command(label="Layout")
settings_menu.add_command(label="Change Database")
menu.add_cascade(label="Settings", menu = settings_menu)
        ##Help Menu#
help_menu = tk.Menu(menu,tearoff = False)
menu.add_cascade(label="Help", menu = help_menu)
help_menu.add_command(label="Controls")
help_menu.add_separator()
help_menu.add_command(label="Mangament System")
window.configure(menu = menu)






#Frame
filter_frame = tk.Frame(window,width=300,height=400, borderwidth= 10)
filter_frame.pack_propagate(False)
filter_frame.pack(side = 'top',fill='both')


# Master setting
    ##Label for the dropbox for finding keywords
filter_label_Manufacture = tk.Label(filter_frame, text="Manufacture", font=("Helvetica", 12))
filter_label_Manufacture.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
filter_label_WidthSize = tk.Label(filter_frame, text="Width Size", font=("Helvetica", 12))
filter_label_WidthSize.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
filter_label_IDNum = tk.Label(filter_frame, text="ID #", font=("Helvetica", 12))
filter_label_IDNum.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'

#TreeView
dataframe = pd.read_csv("Inventory.csv")
table_frame = tk.Frame(master = window,width = 300, height = 500)
table = ttk.Treeview(master = table_frame, columns = tuple(dataframe.columns), show = "headings")
for column in tuple(dataframe.columns):
    table.heading(column, text = column)
    table.column(column, anchor = tk.CENTER)
for rows in dataframe.itertuples(index = False, name = None):
    table.insert(parent = '', index = tk.END,values = tuple(rows))
table_frame.pack(anchor = tk.W, expand = True, fill = "both")
table.pack(anchor = tk.W, fill = "both", expand = True)


    #Dropdown Widgets
choices_Manufacture = ['', 'Shanghai','Fujikura ','SuperPower']
branch1_dropdown = ttk.Combobox(filter_frame, values=choices_Manufacture, width = 11)
branch1_dropdown.pack(anchor=tk.W, padx = 0)

choices_OpCom = ['', '<','>','=','\u2265','\u2264']
branch2_dropdown = ttk.Combobox(filter_frame, values=choices_OpCom,width = 1)
branch2_dropdown.pack(anchor=tk.W)


branch3_dropdown = ttk.Entry(filter_frame, width = 3)
branch3_dropdown.pack(anchor=tk.E)

branch4_dropdown = ttk.Entry(filter_frame, width = 10)
branch4_dropdown.pack(anchor=tk.W)


    #Button Widget
filter_button = ttk.Button(filter_frame, text = 'Filter', command = lambda: filter(dataframe,table,dataframe.columns,[branch1_dropdown.get(),branch3_dropdown.get(),branch4_dropdown.get()]))
filter_button.pack()

# Grid
    #Colums
filter_frame.columnconfigure(0, weight = 1)
filter_frame.columnconfigure(1, weight = 1)
filter_frame.columnconfigure(2, weight = 1)
filter_frame.columnconfigure(3, weight = 1)

    #Rows
filter_frame.rowconfigure(0, weight = 1)


#Placement for the widgets in the grid
##Labels
    ### Labels for the dropdown widgets placements
filter_label_Manufacture.grid(row = 0, column = 0, sticky = 'W')
filter_label_WidthSize.grid(row = 0, column = 1, sticky = 'W', padx =40)
filter_label_IDNum.grid(row = 0, column = 2, sticky = 'W')


    ### Dropdown widgets placements
branch1_dropdown.grid(row = 0, column = 0, sticky = 'e')
branch2_dropdown.grid(row = 0, column = 1, sticky = 'e', padx = 90)
branch3_dropdown.grid(row = 0, column = 1, sticky = 'e', padx = 120)
branch4_dropdown.grid(row = 0, column = 2, sticky = 'w')

    ### Filter button
filter_button.grid(row = 0, column = 4)








#run
window.mainloop()




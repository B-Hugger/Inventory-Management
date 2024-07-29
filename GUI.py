
import tkinter as tk
from tkinter import ttk
import pandas as pd
#import openpyxl

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
filter_frame = tk.Frame(window,width=300,height=400, borderwidth= 10, relief="groove")
filter_frame.pack_propagate(False)
filter_frame.pack(side = 'top',fill='both')


# Master setting
    ##Label for the dropbox for finding keywords
find_label = tk.Label(filter_frame, text="Find:", font=("Helvetica", 14))
find_label.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'

find_label_Manufacture = tk.Label(filter_frame, text="Manufacture", font=("Helvetica", 12))
find_label_Manufacture.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
find_label_WidthSize = tk.Label(filter_frame, text="WidthSize", font=("Helvetica", 12))
find_label_WidthSize.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
find_label_OpCom = tk.Label(filter_frame, text="", font=("Helvetica", 12)) #Operation Comparsion
find_label_OpCom.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
find_label_IDNum = tk.Label(filter_frame, text="ID Number", font=("Helvetica", 12))
find_label_IDNum.pack(anchor=tk.W)  # Use 'tk.W' instead of 'tkinter.W'
#TreeView
dataframe = pd.read_csv("inventory.csv")
table_frame = tk.Frame(master = window,width = 300, height = 500)
table = ttk.Treeview(master = table_frame, columns = tuple(dataframe.columns), show = "headings")
for column in tuple(dataframe.columns):
    table.heading(column, text = column)
    table.column(column, anchor = tk.CENTER)
for rows in dataframe.itertuples(index = False, name = None):
    table.insert(parent = '', index = tk.END,values = tuple(rows))
table_frame.pack(anchor = tk.W, fill = "both")
table.pack(anchor = tk.W, fill = "both")


    #Dropdown Widgets
choices_Manufacture = ['', 'Shanghai','Fujikura ','SuperPower']
branch1_dropdown = ttk.Combobox(filter_frame, values=choices_Manufacture)
branch1_dropdown.pack(anchor=tk.W,padx=10)

choices_OpCom = ['', '<','>','=','</=','>/=']
branch2_dropdown = ttk.Combobox(filter_frame, values=choices_OpCom,width=4)
branch2_dropdown.pack()


branch3_dropdown = ttk.Entry(filter_frame)
branch3_dropdown.pack(anchor=tk.NW, padx=10)




branch4_dropdown = ttk.Entry(filter_frame)
branch4_dropdown.pack(anchor=tk.N,padx=10)
#filter selection
def getValue(filter):
    return filter.get()


    #Button Widget
filter_button = ttk.Button(filter_frame, text = 'Filter', command = lambda: filter(dataframe,table,dataframe.columns,[branch1_dropdown.get(),branch3_dropdown.get(),branch4_dropdown.get()]))
filter_button.pack()
# Grid
    #Colums
filter_frame.columnconfigure(0, weight = 1)
filter_frame.columnconfigure(1, weight = 2)
filter_frame.columnconfigure(2, weight = 1)
filter_frame.columnconfigure(3, weight = 1)
filter_frame.columnconfigure(4, weight = 3)
filter_frame.columnconfigure(5, weight =2)
    #Rows
filter_frame.rowconfigure(0, weight = 1)
filter_frame.rowconfigure(1, weight = 1)
filter_frame.rowconfigure(2, weight = 1)

#Placement for the widgets in the grid
##Labels
    ### The 'Find:' label
find_label.grid(row = 0, column = 0)

    ### Labels for the dropdown widgets placements
find_label_Manufacture.grid(row = 1, column = 1)
find_label_OpCom.grid(row = 1, column = 2)
find_label_WidthSize.grid(row = 1, column = 3)
find_label_IDNum.grid(row = 1, column = 4)

    ### Dropdown widgets placements
branch1_dropdown.grid(row = 2, column = 1)
branch2_dropdown.grid(row = 2, column = 2, sticky = 'e')
branch3_dropdown.grid(row = 2, column = 3)
branch4_dropdown.grid(row = 2, column = 4)

    ### Filter button
filter_button.grid(row = 2, column = 5, padx = 5)



"""
#Label for the dropbox for the adding infromation
add_label = tk.Label(window, text="Add:", font=("Helvetica",18),anchor=tk.W)
add_label.pack()

#Label for the dropbox for deleting and editing
edit_label = tk.Label(window, text="Edit:", font=("Helvetica",18))
edit_label.pack()
"""




#run
window.mainloop()




import tkinter as tk
from tkinter import ttk
import pandas as pd
import customtkinter as ctk
class Application(ctk.CTk):

    def __init__(self, width, height):
        super().__init__()
        self.title("Inventory Management")
        self.geometry(f'{width}x{height}')
        self.configure(fg_color= "#2b2d30")
        self.resizable(False, False)
        self.iconbitmap('ICON.ico')
        #dark_title_bar(self)
        #Menu(self)
        FilterFrame(self, "Inventory.csv")
        self.mainloop()
# def dark_title_bar(window):
#     window.update()
#     DWMWA_USE_IMMERSIVE_DARK_MODE = 20
#     set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
#     get_parent = ct.windll.user32.GetParent
#     hwnd = get_parent(window.winfo_id())
#     rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
#     value = 2
#     value = ct.c_int(value)
#     set_window_attribute(hwnd, rendering_policy, ct.byref(value),
#                          ct.sizeof(value))

class Menu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        settings_menu = tk.Menu(self, tearoff=False)  # contains resolution, layout, change database,etc
        settings_menu.add_command(label="Resolution")
        settings_menu.add_command(label="Layout")
        settings_menu.add_command(label="Change Database")
        self.add_cascade(label="Settings", menu=settings_menu)
        #Help Menu
        help_menu = tk.Menu(self, tearoff=False) #contains controls documentation and general documentation for application
        self.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Controls")
        help_menu.add_separator()
        help_menu.add_command(label="Mangament System")
        parent.configure(menu=self)


class FilterFrame(ctk.CTkFrame):
    def __init__(self, parent, dataframe):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color = "#1e1f22")
        # Frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2,weight = 1)
        self.dataframe = pd.read_csv(dataframe)
        self.pack_propagate(False)
        self.pack( fill='both', expand = True)
        self.createDropdown()
        self.create_table()
        PopUpMenu(table = self.table, filterframe = self)
    def createDropdown(self):
        #create individual frames
        framelist = []
        for index in range(6):
            frame = ctk.CTkFrame(master = self)
            framelist.append(frame)
            if index < 3:
                framelist[index].grid(row = 0, column = index,pady = 15, sticky = "nesw")
                framelist[index].configure(fg_color = "#1e1f22")
            else:
                framelist[index].grid(row = 1, column = index - 3, sticky = "nesw")
                framelist[index].configure(fg_color = "#1e1f22")

        #create entries with labels
        self.entry_dict = {}
        for index, label in enumerate(self.dataframe.columns):
            if index < 6:
                entry_label = ctk.CTkLabel(framelist[index], text=label + ":", font=('Helvetica', 16),
                                           text_color="#afb1b7")
                entry_label.configure(padx=2)
                entry = Entry(parent=framelist[index], column=label, width=90)
                entry.configure(font=('Helvetica', 12), text_color="#afb1b7", fg_color="#2b2d30", height=25, corner_radius= 5)
                if index < 3:
                    entry.pack(anchor="center", side="right")
                    entry_label.pack(anchor = "center", side = "right")
                else:
                    entry.pack(anchor="center", side="right")
                    entry_label.pack(anchor = "center", side = "right")

                self.entry_dict[entry_label] = entry
            else:
                break
        # Button Widget
        filter_button = ctk.CTkButton(self, text='Filter', command=lambda: self.filter(), text_color= "#afb1b7", fg_color= "#2b2d30", hover_color= "#ececec")
        filter_button.grid(row=0, column=3, rowspan = 2)

    def refresh(self, table):
        for row in table.get_children():
            table.delete(row)

    def create_table(self):
        #Table style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1e1f22",
                        foreground="#afb1b7",
                        rowheight=25,
                        fieldbackground="#1e1f22")
        style.map('Treeview', background=[('selected', '#1e1f22')])
        style.configure("Treeview.Heading",
                        background="#1e1f22",
                        foreground="#afb1b7",
                        font=('Arial', 10, 'bold'))
        #Table creation
        table_frame = ctk.CTkFrame(master = self)
        table_frame.grid(row = 2, column = 0, pady=20, ipady=80,columnspan=5,rowspan = 1, sticky="nsew" )
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
        scrollbar_v = ctk.CTkScrollbar(self.table, orientation= "vertical", command = self.table.yview, fg_color= "#1e1f22", button_color= "#afb1b7")
        scrollbar_h = ctk.CTkScrollbar(table_frame, orientation = "horizontal", command = self.table.xview, fg_color= "#1e1f22", button_color= "#afb1b7")
        self.table.configure(yscrollcommand=scrollbar_v.set)
        self.table.configure(xscrollcommand=scrollbar_h.set)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_h.pack(anchor = "s", fill=tk.X)
        #Info display for table
        self.text = tk.StringVar()
        self.text.set("Total Items: " + str(len(self.table.get_children())))
        item_amount = ctk.CTkLabel(master= table_frame, textvariable=self.text, text_color="#afb1b7", fg_color= "#1e1f22" )
        item_amount.pack(anchor = "e", side = "left", fill = "both")
        blank_label = ctk.CTkLabel(master = table_frame, text = "", fg_color= "#1e1f22")
        blank_label.pack(anchor = "w", side = "left", fill = "both", expand = True)

    def filter(self):
        newdataframe = self.dataframe
        columns = self.returnfilters()
        for index, entry in enumerate(columns):
            if entry.get() != '':
                if newdataframe[entry.column].dtype.kind in 'iufc':
                    newdataframe = newdataframe.query(f"{entry.column} {entry.get()}")
                else:
                    newdataframe = newdataframe.query(f"{entry.column} == '{entry.get()}'")

        self.refresh(self.table)
        for rows in newdataframe.itertuples(index=False):
            self.table.insert(parent='', index=tk.END, values=tuple(rows))
        self.text.set("Total Items: " + str(len(self.table.get_children())))

    def refreshTable(self):
        self.refresh(self.table)
        for rows in self.dataframe.itertuples(index=False):
            self.table.insert(parent='', index=tk.END, values=tuple(rows))
        print(self.dataframe.tail())
        self.text.set("Total Items: " + str(len(self.table.get_children())))

    def returnfilters(self):
        list = []
        for key in self.entry_dict.keys():
            list.append(self.entry_dict[key])
        return list

class DropDown(ttk.Combobox):
    def __init__(self, parent, column, width, selections):
        super().__init__(master=parent, width=width, values=selections)
        self.selections = selections
        self.column = column


class Entry(ctk.CTkEntry):
    def __init__(self, parent, column, width):
        super().__init__(master=parent, width=width)
        self.column = column
class PopUpMenu(tk.Menu):
    def __init__(self, table, filterframe):
        super().__init__(filterframe.parent)
        self.filterframe = filterframe
        self.configure(tearoff=False)
        self.add_command(label="Add", command=self.add_data)
        self.add_command(label="Delete", command=self.delete_data)
        self.table = table
        self.table.bind('<Button-3>',self.popup)
    def filler(self):
        print("pressed")
    def popup(self, event):
        # select row under mouse
        self.iid = self.table.identify_row(event.y)
        if self.iid:
            # mouse pointer over item
            self.table.selection_set(self.iid)
            self.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def add_data(self):
        if not any(isinstance(x, tk.Toplevel) for x in self.filterframe.parent.winfo_children()):
                add_window = ctk.CTkToplevel(self.filterframe.parent, fg_color= "#1e1f22")
                add_window.title("Add Data")
                add_window.geometry("300x400")
                add_window.resizable(False, False)
                features_frame = ctk.CTkScrollableFrame(master = add_window, fg_color= "#1e1f22")

                features_frame.pack(side = "left", expand = True, fill = "both")
                label = ctk.CTkLabel(master = features_frame, text="Information: ",font = ('Helvetica', 16),text_color= "#afb1b7" )
                label.grid(row = 0, column = 0, pady = 10)
                self.entry_label = {}
                for index, features in enumerate(self.filterframe.dataframe.columns):
                    label = ctk.CTkLabel(master = features_frame, text=features +":", font = ('Helvetica', 14), text_color= "#afb1b7")
                    entry = ctk.CTkEntry(master = features_frame, fg_color= "#afb1b7")
                    label.grid(row = index + 1, column = 0, pady = 5, sticky = tk.E)
                    entry.grid(row = index + 1, column = 1, sticky = tk.W)
                    self.entry_label[label] = entry
                button = ctk.CTkButton(master = features_frame, text="Add", command= self.add_entry, text_color= "#afb1b7", fg_color= "#2b2d30", hover_color= "#ececec")
                button.grid(row = len(self.entry_label.keys()) + 1, column = 1)
    def add_entry(self):
        data = []
        for label in self.entry_label.keys():
            if self.entry_label[label].get() != '':
                data.append(self.entry_label[label].get())
            else:
                data.append("NaN")
        data = pd.DataFrame([data],columns = self.filterframe.dataframe.columns.values.tolist())
        self.filterframe.dataframe = pd.concat([self.filterframe.dataframe,data], ignore_index = True)
        self.filterframe.dataframe.to_csv("Inventory.csv",mode = 'w', index = False)
        self.filterframe.refreshTable()
    def delete_data(self):
        row_data = self.table.item(self.iid)['values']
        newdataframe = self.filterframe.dataframe
        for index, column in enumerate(self.filterframe.dataframe.columns):
            if self.filterframe.dataframe[column].dtype.kind in 'iufc':
                newdataframe = newdataframe.query(f"{column} == {row_data[index]}")
            else:
                newdataframe = newdataframe.query(f"{column} == '{row_data[index]}'")
        removed_dataframe = pd.merge(self.filterframe.dataframe,newdataframe, on = self.filterframe.dataframe.columns.values.tolist(), how = 'left', indicator = True)
        self.filterframe.dataframe = removed_dataframe[removed_dataframe._merge == 'left_only'].drop(columns = '_merge')
        self.filterframe.dataframe = self.filterframe.dataframe.reset_index(drop = True)
        self.filterframe.dataframe.to_csv("Inventory.csv", mode = "w", index = False)
        self.filterframe.text.set("Total Items: " + str(len(self.table.get_children())))
        self.filterframe.refreshTable()


Application("800", "500")

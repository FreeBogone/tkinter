import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import pandas as pd

data = None # initialize data without any value

#open file and read data
def open_csv_file():
    file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])    
    if file_path:
        data = pd.read_csv(file_path)
        #display_csv_data(data)

# display data in gui
#def display_csv_data(data):
    # under construction


root = tk.Tk()
#-------------------------------------------------------------------------------
# button
button = tk.Button(root, text="Import CSV File", command=open_csv_file)
button.pack(padx=20, pady=10)

# data view
tree = ttk.Treeview(root, show="headings")
tree.pack(padx=20, pady=20, fill="both", expand=True)

# bottom label
status_label = tk.Label(root, text="", padx=20, pady=10)
status_label.pack()
#-------------------------------------------------------------------------------
root.mainloop()


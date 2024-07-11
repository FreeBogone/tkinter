import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

data = None # initialize data without any value

def page1(root):
    page = tk.Frame(root)
    page.grid()
    tk.Label(page, text = 'Login').grid(row = 0)
    
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Label (page, text = 'Username').grid(row = 1, column = 0)
    uname = tk.Entry(page, textvariable=username).grid(row = 1, column = 1)
    tk.Label (page, text = 'Password').grid(row = 2, column = 0)
    pword = tk.Entry(page, textvariable=password).grid(row = 2, column = 1)

    tk.Button(page, text='Login', command=lambda:login(username, password)).grid(row = 3, column = 0)
#end page1

def page2(root):
    page = tk.Frame(root)
    page.grid()
    tk.Label(page, text = 'This is Page 2').grid(row = 0)
    tk.Button(page, text = 'To page 1', command = lambda:changepage('Page1')).grid(row = 1, column = 0)
    tk.Button(page, text = 'To page 3', command = lambda:changepage('Page3')).grid(row = 1, column = 1)
#end page2

def page3(root):
    page = tk.Frame(root)
    page.grid()

    tk.Label(page, text = 'This is page 3').grid(row = 0)
    tk.Button(page, text = 'To page 1', command = lambda:changepage('Page1')).grid(row = 1, column = 0)
    tk.Button(page, text = 'To page 2', command = lambda:changepage('Page2')).grid(row = 1, column = 1)
    
    #import CSV button
    button = tk.Button(root, text="Import CSV File", command=open_csv_file).grid(row = 2, column = 0)
#end page3

# destroys all child widgets of current 
# page and navigates to new page
def changepage(pageName):
    global pagenum, root
    for widget in root.winfo_children():
        widget.destroy()
    if pageName == 'Page1':
        page1(root)
    elif pageName == 'Page2':
        page2(root)
    elif pageName == 'Page3':
        page3(root)
#end changepage

# login
def login(uname, pword):
    print(f'Username: {uname.get()} Password: {pword.get()}')
    changepage('Page2')
#end login

#open file and read data
def open_csv_file():
    file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])    
    if file_path:
        data = pd.read_csv(file_path)
        display_csv_data(data)
#end open_csv_file

# display data in gui
def display_csv_data(data):
 # Convert 'Date' column to datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Extract month and year from Date and create a new column 'YearMonth'
    data['YearMonth'] = data['Date'].dt.to_period('M')

    # Group the data by 'YearMonth' and 'Category' and sum the 'Amount'
    grouped_data = data.groupby(['YearMonth', 'Category'])['Amount'].sum().unstack()

    # Create a new figure and add a subplot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a stacked bar plot of the total amount per category over time
    grouped_data.plot(kind='bar', stacked=True, ax=ax)

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Create a new frame and add it to your Tkinter window
    graph_frame = tk.Frame(root)
    graph_frame.grid(row=3)

    # Create a canvas and add it to your new frame
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#end display_csv_data

# APP START
root = tk.Tk()
page1(root)
root.mainloop()
# END APP START
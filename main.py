import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime

data = None # initialize data without any value

#Login Page
def Login(root):
    page = tk.Frame(root)
    page.grid()
    tk.Label(page, text = 'Login').grid(row = 0)
    
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Label (page, text = 'Username').grid(row = 1, column = 0)
    uname = tk.Entry(page, textvariable=username).grid(row = 1, column = 1)
    tk.Label (page, text = 'Password').grid(row = 2, column = 0)
    pword = tk.Entry(page, textvariable=password).grid(row = 2, column = 1)

    tk.Button(page, text='Login', command=lambda:log_in(username, password)).grid(row = 3, column = 0)
#end Login

def page2(root):
    page = tk.Frame(root)
    page.grid()
    tk.Label(page, text = 'This is Page 2').grid(row = 0)
    tk.Button(page, text = 'To Login Page', command = lambda:changepage('Login')).grid(row = 1, column = 0)
    tk.Button(page, text = 'To page 3', command = lambda:changepage('Page3')).grid(row = 1, column = 1)

    tk.Label(page, text = 'Month:').grid(row = 3, column = 0)
    n = tk.StringVar() 
    monthchoosen = ttk.Combobox(page, width = 15, textvariable = n) 
  
    # Adding combobox drop down list 
    monthchoosen['values'] = ('January',  
                            'February', 
                            'March', 
                            'April', 
                            'May', 
                            'June', 
                            'July', 
                            'August', 
                            'September', 
                            'October', 
                            'November', 
                            'December') 
    monthchoosen.grid(column = 1, row = 3) 
    monthchoosen.current()

    total = tk.StringVar()

    #total in budget for month
    tk.Label(page, text = 'Monthly Total Budget').grid(row = 4, column = 0)
    totalBudget = tk.Entry(page, textvariable=total).grid(row = 4, column = 1)

    tk.Label(page, text = 'Categories', font = ("Arial", 12, "bold"), anchor=tk.CENTER).grid(row = 5, column = 0)
    tk.Button(page, text = 'Add Category', command = lambda:add_category('Add')).grid(row = 6, column = 0)

#end page2

def page3(root):
    page = tk.Frame(root)
    page.grid()

    tk.Label(page, text = 'This is page 3').grid(row = 0)
    tk.Button(page, text = 'To Login Page', command = lambda:changepage('Login')).grid(row = 1, column = 0)
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
    if pageName == 'Login':
        Login(root)
    elif pageName == 'Page2':
        page2(root)
    elif pageName == 'Page3':
        page3(root)
#end changepage

# login
def log_in(uname, pword):
    #print(f'Username: {uname.get()} Password: {pword.get()}')
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
Login(root)
root.mainloop()
# END APP START
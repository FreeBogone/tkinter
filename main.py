import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime

data = None  # initialize data without any value
categories = {}  # Dictionary to store categories and their allocations
monthly_budgets = {}  # Dictionary to store the monthly budgets
monthly_allocations = {}  # Dictionary to store allocations for each month

def set_styles():
    style = ttk.Style()
    style.configure('TFrame', background='white')
    style.configure('TLabel', background='white', foreground='black', font=('Arial', 10))
    style.configure('TButton', background='green', foreground='white', font=('Arial', 10))
    style.map('TButton', background=[('active', 'darkgreen')])
    style.configure('TCombobox', background='white', foreground='black', font=('Arial', 10))

# Login Page
def Login(root):
    page = ttk.Frame(root, padding="10")
    page.pack(expand=True, fill=tk.BOTH)
    
    ttk.Label(page, text='Login').pack(pady=10)

    input_frame = ttk.Frame(page)
    input_frame.pack(pady=10)
    
    ttk.Label(input_frame, text='Username').grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(input_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text='Password').grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(input_frame, show='*')
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Button(page, text='Login', command=lambda: log_in(username_entry.get(), password_entry.get())).pack(pady=10)
# end Login

def page2(root):
    page = ttk.Frame(root, padding="10")
    page.pack(expand=True, fill=tk.BOTH)
    
    ttk.Label(page, text='This is Page 2').pack(pady=10)
    
    nav_frame = ttk.Frame(page)
    nav_frame.pack(pady=10)
    
    ttk.Button(nav_frame, text='To Login Page', command=lambda: changepage('Login')).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(nav_frame, text='To Page 3', command=lambda: changepage('Page3')).grid(row=0, column=1, padx=5, pady=5)
    
    month_frame = ttk.Frame(page)
    month_frame.pack(pady=10)
    
    ttk.Label(month_frame, text='Month:').grid(row=0, column=0, padx=5, pady=5)
    n = tk.StringVar()
    monthchoosen = ttk.Combobox(month_frame, width=15, textvariable=n)
    monthchoosen['values'] = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    monthchoosen.grid(row=0, column=1, padx=5, pady=5)
    monthchoosen.current()
    
    global total
    total = tk.DoubleVar()

    budget_frame = ttk.Frame(page)
    budget_frame.pack(pady=10)
    
    ttk.Label(budget_frame, text='Monthly Total Budget').grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(budget_frame, textvariable=total).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(budget_frame, text='Submit Budget', command=lambda: submit_budget(n.get())).grid(row=0, column=2, padx=5, pady=5)
    
    ttk.Label(page, text='Categories', font=("Arial", 12, "bold")).pack(pady=10)
    ttk.Button(page, text='Add Category', command=add_category).pack(pady=10)
    
    alloc_frame = ttk.Frame(page)
    alloc_frame.pack(pady=10)
    
    ttk.Label(alloc_frame, text='Category').grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(alloc_frame, text='Amount').grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(alloc_frame, text='Allocate Budget', command=allocate_budget).grid(row=1, column=0, columnspan=2, pady=5)
# end page2

def page3(root):
    page = ttk.Frame(root, padding="10")
    page.pack(expand=True, fill=tk.BOTH)
    
    ttk.Label(page, text='This is page 3').pack(pady=10)
    
    nav_frame = ttk.Frame(page)
    nav_frame.pack(pady=10)
    
    ttk.Button(nav_frame, text='To Login Page', command=lambda: changepage('Login')).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(nav_frame, text='To Page 2', command=lambda: changepage('Page2')).grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Button(page, text="Import CSV File", command=open_csv_file).pack(pady=10)
    
    # Button to view budgets
    ttk.Button(page, text="View Monthly Budgets", command=lambda: changepage('ViewBudgets')).pack(pady=10)
# end page3

def CreateAccount(root):
    page = ttk.Frame(root, padding="10")
    page.pack(expand=True, fill=tk.BOTH)
    
    ttk.Label(page, text='Create Account').pack(pady=10)

    input_frame = ttk.Frame(page)
    input_frame.pack(pady=10)
    
    ttk.Label(input_frame, text='Username').grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(input_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text='Password').grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(input_frame, show='*')
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Button(page, text='Create Login', command=lambda: create_login(username_entry.get(), password_entry.get())).pack(pady=10)

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
    elif pageName == 'CreateAccount':
        CreateAccount(root)
    elif pageName == 'ViewBudgets':
        view_budgets(root)
# end changepage

# login
def log_in(uname, pword):
    loginStr = uname + ':' + pword
    f = open('userAuth.txt', 'r')
    for line in f:
        if loginStr in line:
            print(loginStr)
            changepage('Page2')
            return
        else:
            print('Login Information Not Found')

    f.close()
# end login

# create logim
def create_login(uname, pword):
    loginStr = uname + ':' + pword
    f = open('userAuth.txt', 'a')
    f.write('\n' + loginStr)
    f.close() 

    changepage('Login')
# end create login

# Submit Budget
def submit_budget(month):
    if month:
        monthly_budgets[month] = total.get()
        monthly_allocations[month] = {}  # Initialize an empty dictionary for the month
        messagebox.showinfo("Success", f"Monthly total budget for {month} of {monthly_budgets[month]} submitted.")
    else:
        messagebox.showerror("Error", "Please select a month.")
# end submit_budget

# Add Category
def add_category():
    def save_category():
        category_name = category_name_var.get()
        if category_name and category_name not in categories:
            categories[category_name] = 0.0
            messagebox.showinfo("Success", f"Category '{category_name}' added successfully.")
        else:
            messagebox.showerror("Error", "Invalid category name or category already exists.")
        add_cat_win.destroy()

    add_cat_win = tk.Toplevel(root)
    add_cat_win.title("Add Category")
    ttk.Label(add_cat_win, text="Category Name:").grid(row=0, column=0, padx=5, pady=5)
    category_name_var = tk.StringVar()
    ttk.Entry(add_cat_win, textvariable=category_name_var).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(add_cat_win, text="Add", command=save_category).grid(row=1, column=0, columnspan=2, pady=5)
# end add_category

# Allocate Budget
def allocate_budget():
    def save_allocation():
        month = month_var.get()
        if month in monthly_budgets:
            remaining_budget = monthly_budgets[month]
            category_name = category_var.get()
            allocation_amount = allocation_amount_var.get()

            if category_name in categories and allocation_amount > 0:
                if remaining_budget >= allocation_amount:
                    if month not in monthly_allocations:
                        monthly_allocations[month] = {}
                    if category_name in monthly_allocations[month]:
                        monthly_allocations[month][category_name] += allocation_amount
                    else:
                        monthly_allocations[month][category_name] = allocation_amount
                    remaining_budget -= allocation_amount
                    monthly_budgets[month] = remaining_budget
                    messagebox.showinfo("Success", f"Allocated {allocation_amount} to '{category_name}' for {month}. Remaining budget for {month}: {remaining_budget}.")
                else:
                    messagebox.showerror("Error", "Not enough budget remaining.")
            else:
                messagebox.showerror("Error", "Invalid category or allocation amount.")
        else:
            messagebox.showerror("Error", "No budget set for selected month.")
        allocate_win.destroy()

    allocate_win = tk.Toplevel(root)
    allocate_win.title("Allocate Budget")

    ttk.Label(allocate_win, text="Month:").grid(row=0, column=0, padx=5, pady=5)
    month_var = tk.StringVar()
    ttk.OptionMenu(allocate_win, month_var, *monthly_budgets.keys()).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(allocate_win, text="Category:").grid(row=1, column=0, padx=5, pady=5)
    category_var = tk.StringVar()
    ttk.OptionMenu(allocate_win, category_var, *categories.keys()).grid(row=1, column=1, padx=5, pady=5)

    allocation_amount_var = tk.DoubleVar()
    ttk.Label(allocate_win, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(allocate_win, textvariable=allocation_amount_var).grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(allocate_win, text="Allocate", command=save_allocation).grid(row=3, column=0, columnspan=2, pady=5)
# end allocate_budget

def open_csv_file():
    global data
    file_path = filedialog.askopenfilename()
    if file_path:
        data = pd.read_csv(file_path)
        messagebox.showinfo("Success", "CSV file imported successfully.")
# end open_csv_file

def plot_expenses():
    if data is None:
        messagebox.showerror("Error", "No data to plot. Please import a CSV file first.")
        return

    root = tk.Tk()
    root.title("Expenses Over Time")

    figure = plt.Figure(figsize=(8, 6), dpi=100)
    ax = figure.add_subplot(111)
    line = FigureCanvasTkAgg(figure, root)
    line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    data['Date'] = pd.to_datetime(data['Date'])
    data.plot(kind='line', x='Date', y='Amount', ax=ax, color='blue', marker='o')
    ax.set_title('Expenses Over Time')
    ax.set_ylabel('Amount')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.grid(True)

    root.mainloop()
# end plot_expenses

# View Budgets Page
def view_budgets(root):
    page = ttk.Frame(root, padding="10")
    page.pack(expand=True, fill=tk.BOTH)
    
    ttk.Label(page, text='View Monthly Budgets').pack(pady=10)
    
    month_frame = ttk.Frame(page)
    month_frame.pack(pady=10)
    
    ttk.Label(month_frame, text='Month:').grid(row=0, column=0, padx=5, pady=5)
    selected_month = tk.StringVar()
    monthchoosen = ttk.Combobox(month_frame, width=15, textvariable=selected_month)
    monthchoosen['values'] = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    monthchoosen.grid(row=0, column=1, padx=5, pady=5)
    monthchoosen.current()
    
    # Frame for the table and remaining budget
    budget_table_frame = ttk.Frame(page)
    budget_table_frame.pack(pady=10)

    # Table for displaying budget allocations
    columns = ('Category', 'Amount Allocated')
    budget_tree = ttk.Treeview(budget_table_frame, columns=columns, show='headings')
    budget_tree.heading('Category', text='Category')
    budget_tree.heading('Amount Allocated', text='Amount Allocated')
    budget_tree.pack()

    def display_budget():
        # Clear previous entries in the table
        for row in budget_tree.get_children():
            budget_tree.delete(row)
        
        month = selected_month.get()
        if month in monthly_budgets:
            total_budget = monthly_budgets[month]
            allocations = monthly_allocations.get(month, {})
            remaining_budget = total_budget - sum(allocations.values())
            
            # Update table with category allocations
            for category, amount in allocations.items():
                budget_tree.insert('', 'end', values=(category, f"${amount:.2f}"))

            # Show total budget and remaining budget
            ttk.Label(page, text=f"Total Budget for {month}: ${total_budget:.2f}").pack(pady=5)
            ttk.Label(page, text=f"Remaining Budget for {month}: ${remaining_budget:.2f}").pack(pady=5)
        else:
            messagebox.showerror("Error", "No budget set for the selected month.")
        
        # Reset the month selection to the default value
        monthchoosen.current()

    ttk.Button(month_frame, text='Show Budget', command=display_budget).grid(row=1, column=0, columnspan=2, pady=5)
    
    # Function to reset the page
    def reset_page():
        budget_tree.delete(*budget_tree.get_children())
        selected_month.set('')
        monthchoosen.current()
    
    # Add a reset button to clear the view
    ttk.Button(page, text='Reset View', command=reset_page).pack(pady=5)
    
# Main
root = tk.Tk()
root.title("Personal Finance App")
set_styles()

#determine if userAuth file is empty, if empty open Create Login page. if not empty, open login page. This is for security

with open('userAuth.txt', 'r') as f:
    # read first character
    first_char = f.read(1)
 
    if not first_char:
        CreateAccount(root)
    else:
        Login(root)
        
root.mainloop()

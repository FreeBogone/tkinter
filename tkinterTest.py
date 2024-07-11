import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

#open file and read data
def open_csv_file():
    global data
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
    graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create a canvas and add it to your new frame
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#end display_csv_data

root = tk.Tk()
#-------------------------------------------------------------------------------
# button
button = tk.Button(root, text="Import CSV File", command=open_csv_file)
button.pack(padx=20, pady=10)

# bottom label
status_label = tk.Label(root, text="", padx=20, pady=10)
status_label.pack()
#-------------------------------------------------------------------------------
root.mainloop()


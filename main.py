import tkinter as tk
from tkinter import ttk
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saviour lives",
    database="street_light"
)

# Function to add a new street light
def add_light():
    light_id = light_id_entry.get()
    status = status_var.get()
    location = location_entry.get()
    cluster = cluster_entry.get()

    if light_id and status and location and cluster:
        sql = "INSERT INTO street_lights (light_id, light_status, location, cluster) VALUES (%s, %s, %s, %s)"
        val = (light_id, status, location, cluster)

        cursor = mydb.cursor()
        cursor.execute(sql, val)
        mydb.commit()

        load_data()
        clear_entries()
    else:
        tk.messagebox.showerror("Error", "Please fill in all fields.")

# Function to load and display data
def load_data():
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM street_lights")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert('', 'end', values=row)

# Function to search lights by location
def search_location():
    location = location_search_entry.get()

    cursor = mydb.cursor()
    query = "SELECT * FROM street_lights WHERE location LIKE %s"
    cursor.execute(query, ('%' + location + '%',))
    rows = cursor.fetchall()

    load_search_results(rows)

# Function to load search results
def load_search_results(rows):
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    for row in rows:
        tree.insert('', 'end', values=row)

# Function to clear input fields
def clear_entries():
    light_id_entry.delete(0, tk.END)
    status_dropdown.set('')
    location_entry.delete(0, tk.END)
    cluster_entry.delete(0, tk.END)
    location_search_entry.delete(0, tk.END)

# Create main window
window = tk.Tk()
window.title("Street Light Management System")

# Create input fields
light_id_label = ttk.Label(window, text="Light ID:")
light_id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

light_id_entry = ttk.Entry(window)
light_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

status_label = ttk.Label(window, text="Status:")
status_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

status_var = tk.StringVar()
status_dropdown = ttk.Combobox(window, textvariable=status_var, values=["On", "Off", "Burnt", "Healthy"])
status_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

location_label = ttk.Label(window, text="Location:")
location_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

location_entry = ttk.Entry(window)
location_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

cluster_label = ttk.Label(window, text="Cluster:")
cluster_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

cluster_entry = ttk.Entry(window)
cluster_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

# Create tree view to display data
tree = ttk.Treeview(window, columns=("1", "2", "3", "4"), show="headings")
tree.heading("1", text="Light ID")
tree.heading("2", text="Status")
tree.heading("3", text="Location")
tree.heading("4", text="Cluster")
tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# Create buttons
add_button = ttk.Button(window, text="Add Light", command=add_light)
add_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

search_label = ttk.Label(window, text="Search by Location:")
search_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

location_search_entry = ttk.Entry(window)
location_search_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

search_button = ttk.Button(window, text="Search", command=search_location)
search_button.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)

clear_button = ttk.Button(window, text="Clear Entries", command=clear_entries)
clear_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

# Load initial data
load_data()

# Run the main loop
window.mainloop()
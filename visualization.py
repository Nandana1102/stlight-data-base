import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="street_light"
)

# Function to add a new street light
def add_light(tree, light_id_entry, status_var, location_entry, cluster_entry):
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

        # Insert the new data into the Treeview widget
        tree.insert('', 'end', values=(light_id, status, location, cluster))

        clear_entries(light_id_entry, status_var, location_entry, cluster_entry)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# Function to load and display data
def load_data(tree):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM street_lights")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert('', 'end', values=row)

# Function to search lights by location
def search_location(tree, location_search_entry):
    location = location_search_entry.get()

    cursor = mydb.cursor()
    query = "SELECT * FROM street_lights WHERE location LIKE %s"
    cursor.execute(query, ('%' + location + '%',))
    rows = cursor.fetchall()

    load_search_results(tree, rows)

# Function to load all entries
def load_all_entries(tree):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM street_lights")
    rows = cursor.fetchall()

    load_search_results(tree, rows)

# Function to load search results
def load_search_results(tree, rows):
    tree.delete(*tree.get_children())  # Clear the existing data

    for row in rows:
        tree.insert('', 'end', values=row)

# Function to clear input fields
def clear_entries(light_id_entry, status_var, location_entry, cluster_entry):
    light_id_entry.delete(0, tk.END)
    status_var.set('')  # Use set method to clear Combobox
    location_entry.delete(0, tk.END)
    cluster_entry.delete(0, tk.END)

# Function to validate login credentials
def validate_login(username_entry, password_entry, login_window):
    username = username_entry.get()
    password = password_entry.get()

    # Replace these credentials with your actual credentials
    if username == "admin" and password == "admin123":
        login_window.destroy()  # Close the login window
        open_main_window()  # Open the main street light management window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to open the main street light management window
def open_main_window():
    main_window = tk.Tk()
    main_window.title("Street Light Management System")

    # Create input fields for the main window
    light_id_label = ttk.Label(main_window, text="Light ID:")
    light_id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    light_id_entry = ttk.Entry(main_window)
    light_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    status_label = ttk.Label(main_window, text="Status:")
    status_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    status_var = tk.StringVar()
    status_dropdown = ttk.Combobox(main_window, textvariable=status_var, values=["On", "Off", "Burnt", "Healthy"])
    status_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

    location_label = ttk.Label(main_window, text="Location:")
    location_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    location_entry = ttk.Entry(main_window)
    location_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    cluster_label = ttk.Label(main_window, text="Cluster:")
    cluster_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    cluster_entry = ttk.Entry(main_window)
    cluster_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

    # Create tree view to display data
    tree = ttk.Treeview(main_window, columns=("1", "2", "3", "4"), show="headings")
    tree.heading("1", text="Light ID")
    tree.heading("2", text="Status")
    tree.heading("3", text="Location")
    tree.heading("4", text="Cluster")
    tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    # Load initial data
    load_data(tree)  # Pass the 'tree' variable

    # Create buttons
    add_button = ttk.Button(main_window, text="Add Light", command=lambda: add_light(tree, light_id_entry, status_var, location_entry, cluster_entry))
    add_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

    search_label = ttk.Label(main_window, text="Search by Location:")
    search_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

    location_search_entry = ttk.Entry(main_window)
    location_search_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    search_button = ttk.Button(main_window, text="Search", command=lambda: search_location(tree, location_search_entry))
    search_button.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)

    show_all_button = ttk.Button(main_window, text="Show All", command=lambda: load_all_entries(tree))
    show_all_button.grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)

    clear_button = ttk.Button(main_window, text="Clear Entries", command=lambda: clear_entries(light_id_entry, status_var, location_entry, cluster_entry))
    clear_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Create visualization button
    visualize_button = ttk.Button(main_window, text="Visualize Data", command=open_visualization_window)
    visualize_button.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

    # Run the main window loop
    main_window.mainloop()

# Function to open the visualization window
def open_visualization_window():
    visualization_window = tk.Toplevel()
    visualization_window.title("Data Visualization")

    # Create buttons for various visualizations
    pie_chart_button = ttk.Button(visualization_window, text="Pie Chart", command=lambda: show_pie_chart())
    pie_chart_button.pack()

    bar_graph_button = ttk.Button(visualization_window, text="Bar Graph", command=lambda: show_bar_graph())
    bar_graph_button.pack()

    violin_plot_button = ttk.Button(visualization_window, text="Violin Plot", command=lambda: show_violin_plot())
    violin_plot_button.pack()

# Function to show Pie Chart
def show_pie_chart():
    cursor = mydb.cursor()
    cursor.execute("SELECT light_status, COUNT(*) FROM street_lights GROUP BY light_status")
    data = cursor.fetchall()

    status_labels = [status[0] for status in data]
    counts = [count[1] for count in data]

    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=status_labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Street Light Status Distribution")
    plt.show()

# Function to show Bar Graph
def show_bar_graph():
    cursor = mydb.cursor()
    cursor.execute("SELECT location, COUNT(*) FROM street_lights GROUP BY location")
    data = cursor.fetchall()

    locations = [location[0] for location in data]
    counts = [count[1] for count in data]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts, y=locations)
    plt.xlabel("Count")
    plt.ylabel("Location")
    plt.title("Street Lights Count by Location")
    plt.show()

# Function to show Violin Plot
def show_violin_plot():
    cursor = mydb.cursor()
    cursor.execute("SELECT light_status, cluster FROM street_lights")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=["Status", "Cluster"])

    plt.figure(figsize=(10, 6))
    sns.violinplot(x="Status", y="Cluster", data=df)
    plt.xlabel("Status")
    plt.ylabel("Cluster")
    plt.title("Violin Plot of Street Light Status by Cluster")
    plt.show()

# Create login window
login_window = tk.Tk()
login_window.title("Login")

# Create input fields for login window
username_label = ttk.Label(login_window, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

username_entry = ttk.Entry(login_window)
username_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

password_label = ttk.Label(login_window, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

password_entry = ttk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

# Create login button
login_button = ttk.Button(login_window, text="Login", command=lambda: validate_login(username_entry, password_entry, login_window))
login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Run the login window loop
login_window.mainloop()

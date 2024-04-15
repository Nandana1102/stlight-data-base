import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saviour lives",
    database="street_light"
)

# Create a cursor object
cursor = mydb.cursor()

# Execute SQL query to create street_lights table
cursor.execute("CREATE TABLE IF NOT EXISTS street_lights ( \
                light_id INT AUTO_INCREMENT PRIMARY KEY, \
                light_status VARCHAR(255), \
                location VARCHAR(255), \
                cluster VARCHAR(255) \
                )")

# Commit changes
mydb.commit()

# Close cursor and database connection
cursor.close()
mydb.close()

print("Table 'street_lights' created successfully.")

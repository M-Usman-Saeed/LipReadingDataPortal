import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyPassword",
    database="lipReadingDB"
)
cursor = conn.cursor()

# Define the SQL query to test
sql_query = "SELECT * FROM lipReadingDataset_textdata;"

try:
    # Execute the SQL query
    cursor.execute(sql_query)

    # Fetch all the rows from the result
    rows = cursor.fetchall()

    # Print the result
    for row in rows:
        print(row)

except mysql.connector.Error as error:
    # Print any errors that occurred
    print("Error:", error)

finally:
    # Close the database connection
    if conn.is_connected():
        cursor.close()
        conn.close()

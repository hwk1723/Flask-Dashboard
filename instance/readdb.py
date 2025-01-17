import sqlite3

# Connect to the database
conn = sqlite3.connect('expensesDB.db')

# Create a cursor
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Query data from a specific table
cursor.execute("SELECT * FROM income_expenses;")
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()

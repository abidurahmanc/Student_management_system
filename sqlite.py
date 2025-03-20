# import sqlite3

# conn = sqlite3.connect('school_management_demo.db')
# cursor = conn.cursor()

# # Create principal table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS principals (
#     id TEXT PRIMARY KEY,
#     name TEXT NOT NULL,
#     password TEXT NOT NULL
# )
# ''')

# # Create teachers table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS teachers (
#     id TEXT PRIMARY KEY,
#     name TEXT NOT NULL,
#     password TEXT NOT NULL,
#     qualification TEXT,
#     place TEXT,
#     batch TEXT
# )
# ''')

# # Create students table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS students (
#     id TEXT PRIMARY KEY,
#     name TEXT NOT NULL,
#     password TEXT NOT NULL,
#     batch TEXT,
#     python_mark INTEGER,
#     english_mark INTEGER,
#     statistics_mark INTEGER
# )
# ''')

# conn.commit()
# conn.close()
# print("Database and tables created successfully!")

# conn = sqlite3.connect('school_management_demo.db')
# cursor = conn.cursor()

# # Insert a principal
# cursor.execute("INSERT INTO principals (id, name, password) VALUES (?, ?, ?)", 
#                ("admin", "Principal Name", "admin123"))



# conn.commit()
# conn.close()
# print("Users added successfully!")



# adding datas through csv file
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('school_management_demo.db')
cursor = conn.cursor()


file_path = 'students.csv'  
df = pd.read_csv(file_path)  

# Insert data into students table
for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO students (id, name, password, batch, python_mark, english_mark, statistics_mark)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (row['id'], row['name'], row['password'], row['batch'], row['python_mark'], row['english_mark'], row['statistics_mark']))

# Commit and close
conn.commit()
conn.close()

print("Students added successfully!")


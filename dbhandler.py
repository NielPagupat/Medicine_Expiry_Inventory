import sqlite3
from datetime import datetime

# Connect to the SQLite3 database (or create it if it doesn't exist)
def create_connection(db_file="medicine_inventory.db"):
    conn = sqlite3.connect(db_file)
    return conn

# Initialize the database and create the table if it doesn't exist
def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicine_information (
            ID TEXT NOT NULL,
            Batch_No TEXT NOT NULL,
            Medicine_Name TEXT NOT NULL,
            Generic_Name TEXT NOT NULL,
            Pharmaceutical_Name TEXT,
            Expiry_Date TEXT NOT NULL, -- Store dates as TEXT in YYYY-MM-DD format
            Quantity INTEGER NOT NULL,
            PRIMARY KEY (ID, Batch_No)
        )
    ''')
    conn.commit()
    conn.close()

# Add a new record to the medicine_information table
def add_medicine(id_no, batch_no, medicine_name, Generic_Name, pharmaceutical_name, expiry_date, quantity):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medicine_information (ID, Batch_No, Medicine_Name, Generic_Name, Pharmaceutical_Name, Expiry_Date, Quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_no, batch_no, medicine_name, Generic_Name, pharmaceutical_name, expiry_date, quantity))
    conn.commit()
    conn.close()

# Edit an existing record in the medicine_information table by ID
def edit_medicine(id, batch_no, medicine_name=None, Generic_Name=None, pharmaceutical_name=None, expiry_date=None, quantity=None):
    """Edit a medicine record by ID and Batch_No."""
    conn = create_connection()
    cursor = conn.cursor()
    
    # Update only the fields that are provided (not None)
    updates = []
    parameters = []
    
    if medicine_name is not None:
        updates.append("Medicine_Name = ?")
        parameters.append(medicine_name)
    if Generic_Name is not None:
        updates.append("Generic_Name = ?")
        parameters.append(Generic_Name)
    if pharmaceutical_name is not None:
        updates.append("Pharmaceutical_Name = ?")
        parameters.append(pharmaceutical_name)
    if expiry_date is not None:
        updates.append("Expiry_Date = ?")
        parameters.append(expiry_date)
    if quantity is not None:
        updates.append("Quantity = ?")
        parameters.append(quantity)
    
    # Append ID and Batch_No as the final parameters
    parameters.extend([id, batch_no])
    sql = f"UPDATE medicine_information SET {', '.join(updates)} WHERE ID = ? AND Batch_No = ?"
    cursor.execute(sql, parameters)
    conn.commit()
    conn.close()

# Retrieve all records from the medicine_information table
def get_all_medicines():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM medicine_information')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Retrieve a specific record by ID
def get_medicine_by_id_and_batch(id, batch_no):
    """Retrieve a single medicine record by ID and Batch_No."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM medicine_information WHERE ID = ? AND Batch_No = ?', (id, batch_no))
    row = cursor.fetchone()
    conn.close()
    return row

def delete_medicine(id_no, batch_no):
    """Delete a medicine record by ID and Batch_No."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM medicine_information WHERE ID = ? AND Batch_No = ?', (id_no, batch_no))
    conn.commit()
    conn.close()
# Initialize the database (create table if not exists)
initialize_database()

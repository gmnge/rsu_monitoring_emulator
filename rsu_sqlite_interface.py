import sqlite3

def insert_values(db_path, table_name, column_values) -> bool:
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create the INSERT query with placeholders
        query = f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in column_values])})"

        # Execute the query with the provided values
        cursor.execute(query, column_values)

        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()
        return True
    except:
        return False

def update_value(db_path, table_name, column_name, new_value, condition_column, condition_value) -> bool:
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create the UPDATE query with placeholders
        query = f"UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?"

        # Execute the query with the new value and condition value
        cursor.execute(query, (new_value, condition_value))

        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()
    except:
        return False

def is_value_present(db_path, table_name, column_name, condition_value) -> bool:
    # Connect to the SQLite database
    conn = sqlite3.connect('file:'+db_path+'?mode=ro', uri=True)
    cursor = conn.cursor()

    # Check if the value exists in the table
    query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
    cursor.execute(query, (condition_value,))
    existing_row = cursor.fetchone()

    # Close the database connection
    cursor.close()
    conn.close()

    return existing_row

def get_json_table_content(db_path, table) -> list:
    # Connect to the SQLite database
    conn = sqlite3.connect('file:'+db_path+'?mode=ro', uri=True)
    cursor = conn.cursor()

    # Retrieve the lines from the table
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Convert the lines to a JSON list
    results = []
    for row in rows:
        line = {
            'sender': row[0],
            'receiver': row[1],
            'data': eval(row[2]).replace("'", '"'),
            'timestamp': row[3]
            # Add more columns as needed
        }
        results.append(line)

    return results

def get_json_table_lines_condition(db_path, table, column_name, column_value) -> list:
    # Connect to the SQLite database
    conn = sqlite3.connect('file:'+db_path+'?mode=ro', uri=True)
    cursor = conn.cursor()

    # Create the SELECT query with WHERE clause
    query = f"SELECT * FROM {table} WHERE {column_name} = ?"

    # Execute the query with the condition value
    cursor.execute(query, (column_value,))

    # Get the results
    rows = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Convert the lines to a JSON list
    results = []
    for row in rows:
        line = {
            'sender': row[0],
            'receiver': row[1],
            'data': eval(row[2]).replace("'", '"'),
            'timestamp': row[3]
            # Add more columns as needed
        }
        results.append(line)

    return results

def drop_tables(db_path) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute('DROP TABLE device_status')
    except:
        pass
    try:
        conn.execute('CREATE TABLE device_status (sender TEXT PRIMARY KEY, receiver TEXT, data TEXT, timestamp TEXT)')  
    except:
        pass 
    try:
        conn.execute('DROP TABLE comm_data')
    except:
        pass 
    try:
        conn.execute('CREATE TABLE comm_data (sender TEXT, receiver TEXT, data TEXT, timestamp TEXT)')   
    except:
        pass 
    conn.commit()
    conn.close()
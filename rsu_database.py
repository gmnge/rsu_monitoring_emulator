
import rsu_sqlite_interface

database_path = 'data.db'  # Replace with your SQLite database file path
status_table = 'device_status'
logging_table = 'comm_data'

def get_vehicle_list():
    return rsu_sqlite_interface.get_json_table_content(database_path, status_table)

def get_vehicle_logs_json_list(vehicle_name):
    return rsu_sqlite_interface.get_json_table_lines_condition(database_path, logging_table, 'sender', vehicle_name)

def update_vehicle(data):
    # If vehicle already present in status_table, the data is updated and logged
    if rsu_sqlite_interface.is_value_pŕesent(database_path, status_table, 'sender', data[0]):
        # Logging data always appended    
        rsu_sqlite_interface.insert_values(database_path, logging_table, data)        
        # Update the values of the columns in the status table in case it is present
        rsu_sqlite_interface.update_values(database_path, status_table, ('sender', 'receiver', 'data', 'timestamp'), tuple(data), 'sender', data[0])
        # print("updated.")
    
    # In case the line does not exist, the values are inserted in status table and logged
    else:
        # Loggin data always appended
        rsu_sqlite_interface.insert_values(database_path, logging_table, data)
        # Status data only inserted if not present
        rsu_sqlite_interface.insert_values(database_path, status_table, data)
        # print("device inserted.")

def restart_database():
    rsu_sqlite_interface.drop_tables(database_path)
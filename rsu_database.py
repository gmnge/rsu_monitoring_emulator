
import rsu_sqlite_interface

database_path = 'data.db'  # Replace with your SQLite database file path
status_table = 'device_status'
logging_table = 'comm_data'

def get_vehicle_list():
    return rsu_sqlite_interface.get_json_table_content(database_path, status_table)

def get_vehicle_logs_json_list(vehicle_name):
    return rsu_sqlite_interface.get_json_table_lines_condition(database_path, logging_table, 'sender', vehicle_name)

def update_vehicle(message_array):
    # If vehicle already present in status_table, the data is updated and logged
    if rsu_sqlite_interface.is_value_present(database_path, status_table, 'sender', message_array[0]):
        # Status data updated
        rsu_sqlite_interface.update_value(database_path, status_table, 'data', message_array[2], 'sender', message_array[0])
        rsu_sqlite_interface.update_value(database_path, status_table, 'timestamp', message_array[3], 'sender', message_array[0])
        # Logging data always appended    
        rsu_sqlite_interface.insert_values(database_path, logging_table, message_array)   
    
    # In case the line does not exist, the values are inserted in status table and logged
    else:
        # Status data updated
        rsu_sqlite_interface.insert_values(database_path, status_table, message_array)
        # Loggin data always appended
        rsu_sqlite_interface.insert_values(database_path, logging_table, message_array)
        # print("device inserted.")

def restart_database():
    rsu_sqlite_interface.drop_tables(database_path)
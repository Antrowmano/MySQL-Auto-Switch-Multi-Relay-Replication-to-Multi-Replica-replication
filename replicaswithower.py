import pymysql
import time
from cred import Master, replica_user, replica_pass, mysql_servers

max_iterations = 100
iterations = 0

prev_exec_master_log_pos = None
prev_seconds_behind_master = None
prev_master_log_file = None
final_exec_master_log_pos = None
final_master_log_file = None

first_server_config = mysql_servers[0]
try:
    connection = pymysql.connect(
        host=first_server_config['host'],
        user=first_server_config['user'],
        password=first_server_config['password']
    )
    with connection.cursor() as cursor:
        cursor.execute("SHOW SLAVE STATUS")
        result = cursor.fetchone()
        if result:
            print("Replication Status:")
            column_names = [column[0] for column in cursor.description]
            result_dict = dict(zip(column_names, result))
            for column_name, value in result_dict.items():
                ("{column_name}: {value}")
            if result_dict['Slave_IO_Running'] == 'Yes' and result_dict['Slave_SQL_Running'] == 'Yes':
                print("Replication is running")
                while iterations < max_iterations:
                    try:
                        cursor.execute("STOP SLAVE")
                        print("Replication is Stopped in First Server")
                        cursor.execute("SHOW SLAVE STATUS")
                        result = cursor.fetchone()
                        if result:
                            column_names = [i[0] for i in cursor.description]
                            result_dict = dict(zip(column_names, result))
                            master_exec_master_log_pos = result_dict.get('Exec_Master_Log_Pos')
                            seconds_behind_master = result_dict.get('Seconds_Behind_Master')
                            master_master_log_file = result_dict.get('Master_Log_File')
                            master_host = result_dict.get('Master_Host')
                            print(f"Replication Status: Host {master_host} Exec_Master_Log_Pos: {master_exec_master_log_pos}, Seconds_Behind_Master: {seconds_behind_master}, Master_Log_File: {master_master_log_file}")
                            break
                    except pymysql.Error as err:
                        print(f"Error: {err}")
                        break
                    iterations += 1
                    time.sleep(5)
            else:
                print("Replication is not running")
                if result_dict['Slave_IO_Running'] == 'No':
                    print("Slave_IO_Running is No")
                if result_dict['Slave_SQL_Running'] == 'No':
                    print("Slave_SQL_Running is No")
                    print(f"Last_IO_Errno: {result_dict['Last_IO_Errno']}")
                    print(f"Last_IO_Error: {result_dict['Last_IO_Error']}")
                    print(f"Last_SQL_Errno: {result_dict['Last_SQL_Errno']}")
                    print(f"Last_SQL_Error: {result_dict['Last_SQL_Error']}")
        else:
            print("No replication status available")
except pymysql.Error as err:
    print(f"Error: {err}")
for server_config in mysql_servers:
    try: 
        connection = pymysql.connect(
            host=server_config['host'],
            user=server_config['user'],
            password=server_config['password']
        )
        with connection.cursor() as cursor:
            while iterations < max_iterations:
                try:
                    cursor.execute("SHOW SLAVE STATUS")
                    result = cursor.fetchone()
                    if result:
                        column_names = [i[0] for i in cursor.description]
                        result_dict = dict(zip(column_names, result))
                        exec_master_log_pos = result_dict.get('Exec_Master_Log_Pos')
                        seconds_behind_master = result_dict.get('Seconds_Behind_Master')
                        master_log_file = result_dict.get('Master_Log_File')
                        master_host = result_dict.get('Master_Host')
                        if exec_master_log_pos is not None and master_log_file is not None and seconds_behind_master is not None:
                            print(f"Replication Status: Host {master_host} Exec_Master_Log_Pos: {exec_master_log_pos}, Seconds_Behind_Master: {seconds_behind_master}, Master_Log_File: {master_log_file}")
                            if (prev_exec_master_log_pos is not None and prev_exec_master_log_pos == exec_master_log_pos) and \
                                (prev_seconds_behind_master is not None and prev_seconds_behind_master == seconds_behind_master) and \
                                 (prev_master_log_file is not None and prev_master_log_file == master_log_file):
                                print("Replication status has not changed. Stopping the loop.")
                                final_exec_master_log_pos = exec_master_log_pos
                                final_seconds_behind_master = seconds_behind_master
                                final_master_log_file = master_log_file
                                print(f"Replication is Stopped: {master_host}")
                                cursor.execute("STOP SLAVE")
                                cursor.execute(f"CHANGE MASTER TO MASTER_HOST='{Master}',master_user='{replica_user}',master_password='{replica_pass}',MASTER_LOG_FILE='{master_master_log_file}', MASTER_LOG_POS={master_exec_master_log_pos},GET_MASTER_PUBLIC_KEY=1;")
                                print(f"CHANGE MASTER TO executed successfully: {master_host}")
                                cursor.execute("START SLAVE")
                                print(f"Replication is Started: {master_host}")
                                connection.commit()
                                break
                            prev_exec_master_log_pos = exec_master_log_pos
                            prev_seconds_behind_master = seconds_behind_master
                            prev_master_log_file = master_log_file
                        else:
                            print("Exec_Master_Log_Pos or Seconds_Behind_Master not found in the result")
                            break
                    else:
                        print("No result returned from SHOW SLAVE STATUS")
                        break

                    iterations += 1
                    time.sleep(5)
                except pymysql.Error as err:
                    print(f"Error: {err}")
                    break
    except pymysql.Error as err:
        print(f"Error: {err}")
first_server_config = mysql_servers[0]
try:
    connection = pymysql.connect(
        host=first_server_config['host'],
        user=first_server_config['user'],
        password=first_server_config['password']
    )
    with connection.cursor() as cursor:
        cursor.execute("SHOW SLAVE STATUS")
        result = cursor.fetchone()
        if result:
            print("Replication Status:")
            column_names = [column[0] for column in cursor.description]
            result_dict = dict(zip(column_names, result))
            for column_name, value in result_dict.items():
                ("{column_name}: {value}")
            if result_dict['Slave_IO_Running'] == 'Yes' and result_dict['Slave_SQL_Running'] == 'Yes':
                print("Replication is running")
            else:
                print("Replication is not running")
                if result_dict['Slave_IO_Running'] == 'No':
                    print("Slave_IO_Running is No")
                if result_dict['Slave_SQL_Running'] == 'No':
                    print("Slave_SQL_Running is No")
                    print(f"Last_IO_Errno: {result_dict['Last_IO_Errno']}")
                    print(f"Last_IO_Error: {result_dict['Last_IO_Error']}")
                    print(f"Last_SQL_Errno: {result_dict['Last_SQL_Errno']}")
                    print(f"Last_SQL_Error: {result_dict['Last_SQL_Error']}")
                    cursor.execute("START SLAVE")
                    print("Replication is Started")
        else:
            print("No replication status available")
except pymysql.Error as err:
    print(f"Error: {err}")
finally:
    if 'connection' in locals() and connection.open:
        connection.close()
        print("Connection closed")


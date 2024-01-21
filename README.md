MySQL Replication Management Script

Features:

Replication Status Checking: The script checks the replication status of each MySQL server by executing the SHOW SLAVE STATUS query.
Replication Status Management: Based on the replication status, the script can stop or start replication as necessary.
Monitoring: The script monitors the replication status for changes, taking appropriate actions if the status changes.

Usage:

Configuration: Edit the cred.py file to provide the necessary MySQL server credentials (Master, replica_user, replica_pass) and server configurations (mysql_servers).
Execution: Run the script using Python 3.x. Ensure that the pymysql library is installed (pip install pymysql).
Monitoring: Monitor the console output for replication status updates and any errors.

Security Considerations:

Credentials: Avoid hard-coding sensitive information like credentials. Consider using environment variables or other secure methods for storing and retrieving such information.
Access Control: Ensure that the script is executed with appropriate access permissions to interact with the MySQL servers.

Dependencies:

Python 3.x
pymysql library (pip install pymysql)

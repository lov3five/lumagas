import mysql.connector
from mysql.connector import errorcode

def connect_to_mysql(host, database_name, user_name, password):
    """
    Kết nối đến MySQL database.

    Args:
        host (str): địa chỉ host của MySQL database.
        database_name (str): tên của database cần kết nối.
        user_name (str): tên đăng nhập cho MySQL.
        password (str): mật khẩu đăng nhập cho MySQL.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection or None: đối tượng connection cho kết nối thành công hoặc None nếu kết nối thất bại.

    Raises:
        mysql.connector.Error: Nếu kết nối đến database thất bại.
    """
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user_name,
            password=password,
            database=database_name
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        # Check connection
        if mydb.is_connected():
            print("Connecting to MySQL database...")
            db_info = mydb.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            return mydb
        else:
            return None
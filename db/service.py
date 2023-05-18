from prettytable import PrettyTable
from db.connect import mycursor, mydb

# GLOBAL FUNCTION
def get_list_data(name_table, format=False):
    """
    Truy vấn và lấy dữ liệu từ bảng trong cơ sở dữ liệu.

    Args:
        name_table (str): Tên của bảng cần lấy dữ liệu.
        format (bool, optional): Có hiển thị dữ liệu dưới dạng bảng đẹp mắt hay không. Mặc định là False.

    Returns:
        list: Danh sách các bản ghi từ bảng hoặc None nếu không có dữ liệu.

    """
    mycursor.execute("SELECT * FROM {}".format(name_table))
    myresult = mycursor.fetchall()
    mycursor.close()
    if myresult == []:
        print(name_table + ' no data!!!')
        return
    if format == True:
        pretty_table(name_table, mycursor, myresult)
    return myresult


def pretty_table(name_table, cursor, result):
    """In ra bảng dữ liệu với định dạng đẹp.

    Hàm này sử dụng thư viện `prettytable` để in ra bảng dữ liệu với định dạng đẹp.

    Args:
        name_table (str): Tên của bảng cần in ra.
        cursor (Cursor): Đối tượng `Cursor` của `MySQLdb`.

    """
    # Tạo đối tượng PrettyTable
    try:
        x = PrettyTable()
    
        # Tiêu đề bảng
        x.title = name_table.upper()

        # Thiết lập các cột cho bảng
        columns = [i[0] for i in cursor.description]
        x.field_names = columns

        myresult = result
        # Thêm từng bản ghi vào bảng
        for row in myresult:
            x.add_row(row)

        # In bảng với định dạng đẹp của PrettyTable
        print(x)
    except Exception as e:
        print('Error: ' + str(e))
        
# COURSES
def get_all_courses(format=False):
    """ 
    Get all courses

    Keyword arguments:
    format -- True: print table, False: return data (default False)
    """
    try:
        sql = """ 
            select c.name as "course_id", c.classroom_id as "classroom_id", c.instructor_id as "instructor_id", c.instructor_name as "instructor_name", c.subject_id as "subject_id", 
            c.subject_name as "subject_name", c.max_number_of_students as "max_students"
            from courses c 
        """
        
        mycursor.execute(sql)
        
        myresult = mycursor.fetchall()
        
        if myresult == []:
            #print('No data!!!')
            return myresult
        
        elif format == True:
            pretty_table('All courses', mycursor, myresult)
        else:
            return myresult
    except Exception as e:
        print('Error: ' + str(e))
        
def create_course(name, classroom_id, instructor_id, instructor_name, subject_id, subject_name, max_students):
    try:
        sql = "INSERT INTO courses (name, classroom_id, instructor_id, instructor_name, subject_id, subject_name, max_number_of_students) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, classroom_id, instructor_id, instructor_name, subject_id, subject_name, max_students)
        mycursor.execute(sql, val)
    except Exception as e:
        print('Error: ' + str(e))
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    
def delete_all_course():
    try:
        sql = "DELETE FROM courses"
        mycursor.execute(sql)
    except Exception as e:
        print('Error: ' + str(e))
    connect.mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
        
# CLASSES
def create_classes(course_id, room_id, timelesson_id, schedule_id):
    try:
        sql = "INSERT INTO classes (course_id, room_id, timelesson_id, schedule_id) VALUES (%s, %s, %s, %s, %s)"
        val = (id, course_id, room_id, timelesson_id, schedule_id)
        mycursor.execute(sql, val)
    except Exception as e:
        print('Error: ' + str(e))
    connect.mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    
def delete_all_classes():
    try:
        sql = "DELETE FROM classes"
        mycursor.execute(sql)
    except Exception as e:
        print('Error: ' + str(e))
    connect.mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
    
def get_list_classes_by_schedule_id(schedule_id):
    try:
        sql = "SELECT * FROM classes WHERE schedule_id = %s"
        val = (schedule_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return get_list_data(myresult, mycursor)
    except Exception as e:
        print('Error: ' + str(e))
        
def get_list_classes_by_classroom_id(classroom_id):
    try:
        sql = "SELECT * FROM classes WHERE classroom_id = %s"
        val = (classroom_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return get_list_data(myresult, mycursor)
    except Exception as e:
        print('Error: ' + str(e))

# SCHEDULES
def create_new_schedule(fitness):
    
    try:
        sql = "INSERT INTO schedules (fitness) VALUES (%s)"
        val = (fitness,)
        mycursor.execute(sql, val)
    except Exception as e:
        print('Error: ' + str(e))
    connect.mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    
def get_schedule_id_newest():
    try:
        sql = "SELECT id FROM schedules ORDER BY id DESC LIMIT 1"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        return result[0]
    except Exception as e:
        print('Error: ' + str(e))

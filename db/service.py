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
    if myresult == []:
        print(name_table + ' no data!!!')
        return myresult
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
        
def check_data_exist(name_table):
    """Kiểm tra xem bảng có dữ liệu hay không.

    Args:
        name_table (str): Tên của bảng cần kiểm tra.

    Returns:
        bool: True nếu có dữ liệu, False nếu không có dữ liệu.

    """
    mycursor.execute("SELECT * FROM {}".format(name_table))
    myresult = mycursor.fetchall()
    if myresult == []:
        return False
    return True
        
# COURSES
def get_all_courses(format=False):
    """ 
    Get all courses

    Keyword arguments:
    format -- True: print table, False: return data (default False)
    """
    try:
        sql = """ 
            select c.id as "course_id",c.name as "course_name", c.classroom_id as "classroom_id", c.instructor_id as "instructor_id", c.instructor_name as "instructor_name", c.subject_id as "subject_id", 
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
    print(mycursor.rowcount, "record inserted to COURSES.")
    
def delete_all_course():
    try:
            sql = "DELETE FROM courses"
            mycursor.execute(sql)
            mydb.commit()
            print(mycursor.rowcount, "record(s) deleted from COURSES")
    except Exception as e:
        print('Error: ' + str(e))
    
def get_list_courses():
    try:
        sql = "SELECT * FROM courses"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))
        
# CLASSES
def create_classes(course_id, room_id, timelesson_id, schedule_id):
    try:
        sql = "INSERT INTO classes (course_id, room_id, timelesson_id, schedule_id) VALUES (%s, %s, %s, %s)"
        val = (course_id, room_id, timelesson_id, schedule_id)
        mycursor.execute(sql, val)
    except Exception as e:
        print('Error: ' + str(e))
    mydb.commit()
    print(mycursor.rowcount, "record inserted to CLASSES.")
    
def delete_all_classes():
    try:
        sql = "DELETE FROM classes"
        mycursor.execute(sql)
    except Exception as e:
        print('Error: ' + str(e))
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted from CLASSES")
    
def get_list_classes_by_schedule_id(schedule_id):
    try:
        sql = "SELECT * FROM classes WHERE schedule_id = %s"
        val = (schedule_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))
        
def get_list_classes_by_schedule_best():
    try:
        schedule_id = get_schedule_id_newest()
        sql = """SELECT c2.name, c2.subject_name, c2.classroom_id, 
        c2.instructor_name , r.name, t.period, c2.max_number_of_students, r.capacity 
                FROM classes c
                JOIN courses c2 on c.course_id = c2.id 
                JOIN rooms r on c.room_id = r.id 
                JOIN timelessons t on c.timelesson_id = t.id
                WHERE schedule_id = %s"""
        val = (schedule_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))
        
def get_list_classes_for_export_schedule_best():
    try:
        schedule_id = get_schedule_id_newest()
        sql = """SELECT c2.name, c2.classroom_id, c2.instructor_id , c2.instructor_name , c2.subject_id , c2.subject_name , c2.max_number_of_students , r.name , r.capacity, r.`type` , t.uuid , t.period 
                FROM classes c
                JOIN courses c2 on c.course_id = c2.id 
                JOIN rooms r on c.room_id = r.id 
                JOIN timelessons t on c.timelesson_id = t.id
                WHERE schedule_id = %s"""
        val = (schedule_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))
        
        
def get_list_classes_by_classroom_id(classroom_id):
    try:
        schedule_id = get_schedule_id_newest()
        sql = sql = """SELECT c2.name, c2.classroom_id, c2.instructor_id , c2.instructor_name , c2.subject_id , c2.subject_name , c2.max_number_of_students , r.name , r.capacity, r.`type` , t.uuid , t.period 
                FROM classes c
                JOIN courses c2 on c.course_id = c2.id 
                JOIN rooms r on c.room_id = r.id 
                JOIN timelessons t on c.timelesson_id = t.id
                WHERE c2.classroom_id = %s and c.schedule_id = %s"""
        val = (classroom_id, schedule_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))
        
def get_list_classes_by_instructor_id(instructor_id):
    try:
        schedule_id = get_schedule_id_newest()
        sql = sql = """SELECT c2.name, c2.classroom_id, c2.instructor_id , c2.instructor_name , c2.subject_id , c2.subject_name , c2.max_number_of_students , r.name , r.capacity, r.`type` , t.uuid , t.period 
                FROM classes c
                JOIN courses c2 on c.course_id = c2.id 
                JOIN rooms r on c.room_id = r.id 
                JOIN timelessons t on c.timelesson_id = t.id
                WHERE c2.instructor_id = %s and c.schedule_id = %s
                """
        val = (instructor_id, schedule_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))
        
def get_room_id_from_list_classes():
    try:
        sql = "SELECT DISTINCT room_id FROM classes"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))
        
def get_list_classroom_newest():
    try:
        schedule_id = get_schedule_id_newest()
        sql = """SELECT c2.classroom_id 
                FROM classes c 
                JOIN courses c2 ON c.course_id = c2.id 
                WHERE c.schedule_id = %s
                GROUP BY c2.classroom_id"""
        val = (schedule_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))
        
def get_list_instructor_newest():
    try:
        schedule_id = get_schedule_id_newest()
        sql = """SELECT c2.instructor_id 
                FROM classes c 
                JOIN courses c2 ON c.course_id = c2.id 
                WHERE c.schedule_id = %s
                GROUP BY c2.instructor_id """
        val = (schedule_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))
        


# SCHEDULES
def create_new_schedule(fitness, running_time, population_size, mutation_rate, crossover_rate, conflict):
    try:
        sql = "INSERT INTO schedules (fitness, running_time, population_size, mutation_rate, crossover_rate, conflict) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (fitness ,running_time, population_size, mutation_rate, crossover_rate, conflict)
        mycursor.execute(sql, val)
    except Exception as e:
        print('Error: ' + str(e))
    mydb.commit()
    print(mycursor.rowcount, "record inserted to SCHEDULES.")
    
def get_schedule_id_newest():
    try:
        sql = "SELECT id FROM schedules ORDER BY id DESC LIMIT 1"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult[0][0]
    except Exception as e:
        print('Error: ' + str(e))
        

        
def delete_schedule_by_id(schedule_id):
    try:
        sql = "DELETE FROM schedules WHERE id = %s"
        val = (schedule_id,)
        mycursor.execute(sql, val)
    except Exception as e:
        print('Error: ' + str(e))
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted from SCHEDULES")


def get_list_schedules_create_nearly():
    try:
        schedule_id = get_schedule_id_newest()
        sql = "SELECT * FROM schedules WHERE id = %s"
        val = (schedule_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))

# ROOMS 
def get_list_rooms():
    try:
        sql = "SELECT * FROM rooms"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))

def create_room(name, capacity, type):
    try:
        sql = "INSERT INTO rooms (name, capacity, type) VALUES (%s, %s, %s)"
        val = (name, capacity, type)
        mycursor.execute(sql, val)
    except Exception as e:
        print('Error: ' + str(e))
    mydb.commit()
    print(mycursor.rowcount, "record inserted to ROOMS.")
    

def delete_all_room():
    try:
        sql = "DELETE FROM rooms"
        mycursor.execute(sql)
    except Exception as e:
        print('Error: ' + str(e))
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted from ROOMS")
    
def get_capacity_by_room_id(room_id):
    try:
        sql = "SELECT capacity FROM rooms WHERE name = %s"
        val = (room_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult[0][0]
    except Exception as e:
        print('Error: ' + str(e))

# TIMELESSONS
def get_list_timelessons():
    try:
        sql = "SELECT * FROM timelessons"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult
    except Exception as e:
        print('Error: ' + str(e))

def create_timelesson(uuid, period):
    try:
        sql = "INSERT INTO timelessons (uuid, period) VALUES (%s, %s)"
        val = (uuid, period)
        mycursor.execute(sql, val)
    except Exception as e:
        print('Error: ' + str(e))
    mydb.commit()
    print(mycursor.rowcount, "record inserted to TIMELESSONS.")
    
def delete_all_timelesson():
    try:
        sql = "DELETE FROM timelessons"
        mycursor.execute(sql)
    except Exception as e:
        print('Error: ' + str(e))
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted from TIMELESSONS")

def courses_per_resource(courses, rooms, time_lessons):
    if rooms is None or time_lessons is None:
        return ("courses_per_resource: {} / {}".format(len(courses), 0))
    return ("courses_per_resource: {} / {}".format(len(courses), len(rooms) * len(time_lessons)))


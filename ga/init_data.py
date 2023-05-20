from ga.course import init_courses
from ga.room import init_rooms
from ga.timelesson import init_timelessons

from db.service import get_all_courses, get_list_data

# Kiểm tra dữ liệu đầu vào đảm bảo cho thuật toán chạy
def validate_data():
    courses_db, rooms_db, timelessons_db = get_data_from_db()
    if len(courses_db) == 0:
        return False, "Bạn chưa import dữ liệu lớp học phần (COURSES)"
    elif len(rooms_db) == 0:
        return False, "Bạn chưa import dữ liệu phòng học (ROOMS)"
    elif len(timelessons_db) == 0:
        return False, "Bạn chưa import dữ liệu thời gian học (TIMELESSONS)"
    elif len(courses_db) > (len(rooms_db) * len(timelessons_db)):
        return False, "[Số lượng lớp học phần (COURSES)] > [số lượng phòng học (ROOMS)] x [số lượng thời gian học (TIMELESSONS)]"
    else:
        return True, "OK"

# Lấy dữ liệu mới nhất từ database
def get_data_from_db():
    courses_db = get_all_courses()
    rooms_db = get_list_data('rooms')
    timelessons_db = get_list_data('timelessons')
    return courses_db, rooms_db, timelessons_db

# Lấy dữ liệu từ user và khởi tạo các đối tượng để chạy thuật toán
def get_data_input_of_user_from_db_and_init():
    courses_db, rooms_db, timelessons_db = get_data_from_db()
    print("courses_db: ", courses_db)
    courses_db_global = init_courses(courses_db)
    rooms_db_global = init_rooms(rooms_db)
    timelessons_db_global = init_timelessons(timelessons_db)
    
    return courses_db_global, rooms_db_global, timelessons_db_global
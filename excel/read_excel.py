import pandas as pd
from prettytable import PrettyTable

from utils.print_column import print_list_one_column

from db.service import create_course, create_room, create_timelesson, delete_all_course, delete_all_room, delete_all_timelesson, get_list_courses, get_list_timelessons, get_list_rooms, delete_all_classes

# Đọc dữ liệu từ tệp tin Excel
def check_file_data_input(template_df, df):
    # Trích xuất các tên cột từ tệp tin template
    expected_columns = list(template_df.columns)
    actual_columns = list(df.columns)
    # Tìm các cột không khớp với mẫu
    mismatched_columns = [column for column in expected_columns if column not in actual_columns]

    # Các cột dư thừa
    extra_columns = [column for column in actual_columns if column not in expected_columns]
    column_error = 0
    if mismatched_columns or extra_columns:
        print("Tệp tin Excel không khớp với mẫu.")
        if mismatched_columns:
            print("Các cột sau đây không tìm thấy:")
            error_msg = 'Các cột sau đây không giống với mẫu: ' + ', '.join(str(x) for x in mismatched_columns)
            column_error = 1
            print_list_one_column(mismatched_columns)
            return False, error_msg
        if extra_columns:
            print("Các cột sau đây là dư thừa:")
            error_msg = 'Các cột sau đây là dư thừa: ' + ', '.join(str(x) for x in extra_columns)
            column_error = 1
            print_list_one_column(extra_columns)
            return False, error_msg
    
    # Kiểm tra hàng có giá trị bị thiếu (NaN)
    if column_error == 0:
        missing_values = df.isnull().sum(axis=1)
        missing_rows = df[missing_values > 0]
        if not missing_rows.empty:
            print("Các hàng sau đây có giá trị bị thiếu:")
            error_msg = 'Các hàng sau đây có giá trị bị thiếu: ' + ', '.join(str(x) for x in missing_rows)
            x = PrettyTable()
            x.field_names = ['STT'] + list(missing_rows.columns)
            for index, row in missing_rows.iterrows():
                x.add_row([index + 2] + list(row))
            print(x)
            print("Vui lòng kiểm tra lại tệp tin Excel.")
            return False, error_msg
        else:
            print("Tệp Excel hợp lệ.")
            valid_msg = 'Tệp Excel hợp lệ.'
            return True, valid_msg


            
# Đọc file course và lưu vào db
def read_and_save_course_to_db(template_df, df):
    # Đọc tệp tin template.xlsx
    course_template_df = template_df
    # Đọc tệp tin data_course_input
    course_df = df
    #print(len(get_list_courses()))
    if len(get_list_courses()) > 0:
        delete_all_classes()
        delete_all_course()
    # Đọc dữ liệu từ tệp tin Excel
        if course_df is not None:
            expected_columns = list(course_template_df.columns)
            # Thêm các danh sách các khóa học vào db
            for index, row in course_df.iterrows():
                create_course(row[expected_columns[0]], row[expected_columns[1]], row[expected_columns[2]], row[expected_columns[3]], row[expected_columns[4]], row[expected_columns[5]] ,row[expected_columns[6]])
    
            
#Đọc file rooms và lưu vào db
def read_and_save_room_to_db(template_df, df):
    # Đọc tệp tin template.xlsx
    room_template_df = template_df
    
    # Đọc dữ liệu từ tệp Excel
    room_df = df
    if len(get_list_rooms()) > 0:
        delete_all_classes()
        delete_all_room()
        if room_df is not None:
            expected_columns = list(room_template_df.columns)
            # Thêm các danh sách các phòng học vào db
            for index, row in room_df.iterrows():
                create_room(row[expected_columns[0]], row[expected_columns[1]], row[expected_columns[2]])
                
def read_and_save_timelesson_to_db(template_df, df):
    # Đọc tệp tin template.xlsx
    timelesson_template_df = template_df
    
    # Đọc dữ liệu từ tệp Excel
    timelesson_df = df
    if len(get_list_timelessons()) != 0:
        delete_all_classes()
        delete_all_timelesson()
        if timelesson_df is not None:
            expected_columns = list(timelesson_template_df.columns)
            print(expected_columns)
            # Thêm các danh sách các thời gian học vào db
            for index, row in timelesson_df.iterrows():
                create_timelesson(row[expected_columns[0]], row[expected_columns[1]])

def save_file_upload_to_db(type_data, template_df, df):
    if type_data == 'course':
        read_and_save_course_to_db(template_df, df)
    elif type_data == 'room':
        read_and_save_room_to_db(template_df, df)
    elif type_data == 'timelesson':
        read_and_save_timelesson_to_db(template_df, df)
    else:
        print('Không tìm thấy loại dữ liệu.')

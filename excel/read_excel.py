import pandas as pd
from prettytable import PrettyTable

from utils.print_column import print_list_one_column

from db.service import create_course, create_classes, create_room, create_timelesson

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
            column_error = 1
            print_list_one_column(mismatched_columns)
            return False
        if extra_columns:
            print("Các cột sau đây là dư thừa:")
            column_error = 1
            print_list_one_column(extra_columns)
            return False
    
    # Kiểm tra hàng có giá trị bị thiếu (NaN)
    if column_error == 0:
        missing_values = df.isnull().sum(axis=1)
        missing_rows = df[missing_values > 0]
        if not missing_rows.empty:
            print("Các hàng sau đây có giá trị bị thiếu:")
            x = PrettyTable()
            x.field_names = ['STT'] + list(missing_rows.columns)
            for index, row in missing_rows.iterrows():
                x.add_row([index + 2] + list(row))
            print(x)
            print("Vui lòng kiểm tra lại tệp tin Excel.")
            return False
        else:
            print("Tệp Excel hợp lệ.")
            return True


            
# Đọc file course và lưu vào db
def read_and_save_course_to_db(file_path):
    # Đọc tệp tin template.xlsx
    course_template_df = pd.read_excel('./app/static/file/templates/course_template.xlsx')
    # Đọc tệp tin data_course_input
    course_df = pd.read_excel(file_path)

    # Đọc dữ liệu từ tệp tin Excel
    if course_df is not None:
        if check_file_data_input(course_template_df, course_df):
            expected_columns = list(course_template_df.columns)
            # Thêm các danh sách các khóa học vào db
            for index, row in course_df.iterrows():
                create_course(row[expected_columns[0]], row[expected_columns[1]], row[expected_columns[2]], row[expected_columns[3]], row[expected_columns[4]], row[expected_columns[5]] ,row[expected_columns[6]])
    
            
#Đọc file rooms và lưu vào db
def read_and_save_room_to_db(file_path):
    # Đọc tệp tin template.xlsx
    room_template_df = pd.read_excel('./app/static/file/templates/room_template.xlsx')
    
    # Đọc dữ liệu từ tệp Excel
    room_df = pd.read_excel(file_path)
    
    if room_df is not None and check_file_data_input(room_template_df, room_df):
        expected_columns = list(room_template_df.columns)
        # Thêm các danh sách các phòng học vào db
        for index, row in room_df.iterrows():
            create_room(row[expected_columns[0]], row[expected_columns[1]], row[expected_columns[2]])
                
def read_and_save_timelesson_to_db(file_path):
    # Đọc tệp tin template.xlsx
    timelesson_template_df = pd.read_excel('./app/static/file/templates/timelesson_template.xlsx')
    
    # Đọc dữ liệu từ tệp Excel
    timelesson_df = pd.read_excel(file_path)

    if timelesson_df is not None and check_file_data_input(timelesson_template_df, timelesson_df):
        expected_columns = list(timelesson_template_df.columns)
        print(expected_columns)
        # Thêm các danh sách các thời gian học vào db
        for index, row in timelesson_df.iterrows():
            create_timelesson(row[expected_columns[0]], row[expected_columns[1]])
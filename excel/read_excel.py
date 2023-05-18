import pandas as pd
from prettytable import PrettyTable

from utils.print_column import print_list_one_column

from db.service import create_course

def read_course_data_input(template_df, df):
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
        if extra_columns:
            print("Các cột sau đây là dư thừa:")
            column_error = 1
            print_list_one_column(extra_columns)

    
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
    
    
    # Kiểm tra ràng buộc dữ liệu
    # 'Số_lượng_sinh_viên' có giá trị âm hay không
    negative_values = df[df['Số_lượng_sinh_viên'] < 0]
    if not negative_values.empty:
        print("Các hàng sau đây có 'Số_lượng_sinh_viên' là giá trị âm:")
        x = PrettyTable()
        x.field_names = ['STT'] + list(negative_values.columns)
        for index, row in negative_values.iterrows():
            x.add_row([index + 2] + list(row))
        print(x)
    
    else:
        print("Tệp Excel hợp lệ.")
        for index, row in df.iterrows():
            create_course(row[expected_columns[0]], row[expected_columns[1]], row[expected_columns[2]], row[expected_columns[3]], row[expected_columns[4]], row[expected_columns[5]], row[expected_columns[6]])

# import os
# os.append.path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
def add_dataframe_to_excel(file_path, list_name_column, list_data, new_sheet_name=None):
    """
    Thêm một DataFrame vào một trang tính mới của một tệp Excel đã có các trang tính.

    Parameters:
    file_path (str): Đường dẫn đến tệp Excel.
    list_name_column (list): Danh sách tên cột.
    list_data (list): Danh sách dữ liệu.
    new_sheet_name (str, optional): Tên của trang tính mới. Mặc định là None.

    Returns:
    pandas.DataFrame: DataFrame mới được tạo từ tệp Excel đã cập nhật.
    """
    # Ghi DataFrame mới vào trang tính mới của tệp Excel đã có sẵn
    df = pd.DataFrame(list_data, columns=list_name_column)
    if new_sheet_name is None:
        new_sheet_name = 'Sheet1'
        if new_sheet_name in pd.ExcelFile(file_path).sheet_names:
            # Tạo tên trang tính mới dựa trên tên hiện tại
            base_sheet_name = new_sheet_name
            count = 2
            while new_sheet_name in pd.ExcelFile(file_path).sheet_names:
                new_sheet_name = base_sheet_name + str(count)
                count += 1

    if not os.path.isfile(file_path):
        # Tạo tệp Excel mới nếu tệp không tồn tại
        with pd.ExcelWriter(file_path) as writer:
            df.to_excel(writer, sheet_name=new_sheet_name, index=False)
    else:
        # Ghi DataFrame mới vào trang tính mới của tệp Excel đã có sẵn
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=new_sheet_name, index=False)

    # Đọc tệp Excel đã cập nhật hoặc mới tạo và trả về DataFrame mới
    with pd.ExcelFile(file_path) as xls:
        sheet_names = xls.sheet_names
        dfs = []
        for sheet_name in sheet_names:
            df = pd.read_excel(xls, sheet_name)
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)
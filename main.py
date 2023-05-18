import os
import sys
import pandas as pd
# Lấy đường dẫn gốc của dự án
project_root = os.path.dirname(os.path.abspath(__file__))
# Thêm đường dẫn gốc vào PYTHONPATH
sys.path.append(project_root)

from db.service import get_list_data

# IMPORT EXCEL FILE PROCESSING
from excel.read_excel import read_course_data_input

# IMPORT FLASK APP
from app.app import app


# Đọc tệp tin template.xlsx
course_template_df = pd.read_excel('./app/static/file/templates/course_template.xlsx')
# ĐỌc tệp tin data_course_input.title
course_df = pd.read_excel('./excel/data_input/course_test.xlsx')

read_course_data_input(course_template_df, course_df)




if __name__ == '__main__':
    app.run()
    #

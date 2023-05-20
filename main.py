import os
import sys
import pandas as pd
# Lấy đường dẫn gốc của dự án
project_root = os.path.dirname(os.path.abspath(__file__))
# Thêm đường dẫn gốc vào PYTHONPATH
sys.path.append(project_root)

# IMPORT FLASK APP
from app.app import app

if __name__ == '__main__':
    app.run(debug=True)


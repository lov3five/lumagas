import os

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename
app = Flask(__name__, static_url_path='/static')

# IMPORT DB SERVICE
from db.service import *

# Lấy đường dẫn gốc của dự án
project_root = os.path.dirname(os.path.abspath(__file__))

#TEST
@app.route('/api/test', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, world!'})

# GET homepage LUMAGAS
@app.route('/')
def index():
    return render_template('index.html')

# GA Module support
import time

from prettytable import PrettyTable

from ga.ga import GA
from ga.population import Population
from utils.display_prettytable import display_result
from utils.sound_notification import sound_notification

# TEST API
""" GET """
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'result': 'success'}), 200

# API get list of schedule best fitness from database
from db.service import get_list_classes_by_schedule_id_newest


@app.route('/api/schedule', methods=['GET'])
def get_schedules(): 
    schedule = []
    for i in range(0, len(get_list_classes_by_schedule_id_newest())):
        schedule.append({
            'maHocPhan': get_list_classes_by_schedule_id_newest()[i][0],
            'tenHocPhan': get_list_classes_by_schedule_id_newest()[i][1],
            'tenLopHoc': get_list_classes_by_schedule_id_newest()[i][2],
            'tenGiangVien': get_list_classes_by_schedule_id_newest()[i][3],
            'tenPhongHoc': get_list_classes_by_schedule_id_newest()[i][4],
            'thoiGianHoc': get_list_classes_by_schedule_id_newest()[i][5],
        })
    return jsonify({'result': schedule, 'data': get_list_classes_by_schedule_id_newest()}), 200

# API start GA algorithm
#@app.route('/api/start-ga', methods['POST'])
from ga.init_data import *
    
@app.route('/api/ga/start', methods=['GET'])
def run_genetic_algorithm():
    # Kiểm tra điều kiện dữ liệu
    courses, rooms, timelessons = get_data_input_of_user_from_db_and_init()
    print("============================================", courses, rooms, timelessons)
    is_passed, message = validate_data()
    if is_passed == False:
        return jsonify({'result': 'Dữ liệu không hợp lệ', 'message': message}), 400
    else:
        # Lấy các thông số chạy GA từ yêu cầu POST
        #data = request.get_json()
        best_fitness = 0
        # xác định dân số ban đầu của quần thể
        population_size = 50
    
        # xác định số thế hệ (lần lặp lại) thuật toán
        num_generations = 20000
        # Tỉ lệ đột biến
        mutation_rate = 0.1 # 0.01 - 0.1
        # Tỉ lệ lai ghép
        crossover_rate = 0.85  # 0.6 - 0.9
        elitism_rate = 0.1 # 0.05 - 0.1
        
        # Lấy dữ liệu từ user
        courses, rooms, timelessons = get_data_input_of_user_from_db_and_init()
        print("============================================")
        # Tạo quần thể ban đầu
        # Bắt đầu tính thời gian chạy thuật toán
        start_time = time.time()
        
        population = Population(population_size, courses, rooms, timelessons).get_schedules()
        print("Cá thể tốt nhất trong quần thể ban đầu:")
        print(display_result(population))
    
        ga = GA(population, mutation_rate, crossover_rate, elitism_rate, courses, rooms, timelessons)
    
        population_result = ga.run(num_generations)
        unchanged_conflict_count = ga.get_unchanged_count()
        # Lấy ra kết quả tốt nhất
        best_schedule = ga.get_population()
        for schedule in best_schedule:
            list_conflict_of_schedule = []
            list_fitness_of_schedule = []
            list_conflict_of_schedule.append(schedule.get_conflict())
            list_fitness_of_schedule.append(schedule.get_fitness())

        x = PrettyTable()
        x.field_names = ["Schedule ID", "Conflict", "Fitness"]
        for i in range(0, len(list_conflict_of_schedule)):
            x.add_row([i, list_conflict_of_schedule[i], list_fitness_of_schedule[i]])
        print(x)

        print("Best schedule: ", best_schedule[0])
        
        # Kết thúc tính thời gian chạy thuật toán
        end_time = time.time()
        
        # Tính thời gian chạy thuật toán
        running_time = end_time - start_time
        print("Time: ", end_time - start_time)
        if ga.get_population()[0].get_conflict() == 0 or (unchanged_conflict_count > 150 and running_time > 300) :
            #sound_notification()
            population_result.sort(key=lambda x: x.get_fitness(), reverse=True)
            print('Best schedule fitness: ', population_result[0].get_fitness())
            display_result(population_result)
            # Lưu những kết quả tốt nhất vào database
            # Lưu schedule vào database
            # Lấy những thông tin cần lưu
            fitness = population_result[0].get_fitness()
        
            create_new_schedule(fitness, running_time, population_size, mutation_rate, crossover_rate)
            schedule_id = get_schedule_id_newest()
            # Lưu classes vào database
            for i in range(0, len(population_result[0].get_classes())):
                course_id = population_result[0].get_classes()[i].get_course().get_course_id()
                room_id = population_result[0].get_classes()[i].get_room().get_room_id()
                timelesson_id = population_result[0].get_classes()[i].get_timelesson().get_timelesson_id()
                create_classes(course_id, room_id, timelesson_id, schedule_id)
            # Nếu các classes không lưu vào db, xóa schedule vừa lưu
            if get_list_classes_by_schedule_id(schedule_id) == []:
                delete_schedule_by_id(schedule_id)
        return jsonify({'result': 'success', 'unchanged_conflict_count': unchanged_conflict_count}), 200
    
# API get index input of GA: population size, mutation rate, crossover rate
#@app.route('/api/ga/result-analysis', methods=['GET'])
#def get_result_analysis():


""" POST """
### UPLOAD FILE EXCEL
INPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../excel/data_input')
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../excel/data_output')
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

app.config['UPLOAD_FOLDER'] = INPUT_FOLDER
app.config['DOWNLOAD_FOLDER'] = OUTPUT_FOLDER

import pandas as pd

from excel.config_api_template import check_api_and_select_template_to_compare
from excel.read_excel import check_file_data_input, save_file_upload_to_db


# Kiểm tra file có đúng định dạng không
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Tạo tên file mới nếu trùng tên file đã có trong thư mục upload
def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename  # Đặt giá trị mặc định cho new_filename
    # Nếu filename chưa có trong thư mục upload thì giữ nguyên
    if not os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)):
        return new_filename
    while True:
        new_filename = "{}_{}{}".format(base, counter, ext)
        if not os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)):
            break
        counter += 1
    return new_filename

# API upload file excel support 3 object course, room, timelesson
@app.route('/api/upload/<type_data>', methods=['POST'])
# http://127.0.0.1:5000/api/upload/course
# http://127.0.0.1:5000/api/upload/room
# http://127.0.0.1:5000/api/upload/timelesson
def upload_file(type_data):
    file = request.files['file']
    # Kiểm tra xem request POST có chứa phần file không
    if 'file' not in request.files:
        return jsonify({'result': 'Không có tệp từ yêu cầu'}), 400
    # Nếu người dùng không chọn file, trình duyệt gửi file trống không có tên file
    if file.filename == '':
        return jsonify({'result': 'Không có tệp nào được chọn để tải lên'}), 400
    
    if len(request.files.getlist('file')) != 1:
        return jsonify({'result': 'Vui lòng chỉ tải lên một tệp'}), 400
    
    if request.method == 'POST' and file and allowed_file(file.filename):
        # Đọc file mẫu dựa trên loại dữ liệu
        template_df = check_api_and_select_template_to_compare(type_data)
        df = pd.read_excel(file)
        if df is None:
            return jsonify({'result': 'Loại dữ liệu không hợp lệ'}), 400
        # Kiểm tra file đầu vào và trả lỗi 
        is_valid, error_data = check_file_data_input(df, template_df)
        # is_valid = True | False
        if is_valid: 
            # Lưu file vào thư mục
            filename = secure_filename(file.filename)
            unique_filename = get_unique_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            # Lưu file vào database
            save_file_upload_to_db(type_data, template_df, df)
            return jsonify({'result': 'Tệp đã tải lên thành công với tên: ' + unique_filename}), 200
        else: 
            if error_data is not None:
                return jsonify({'result': error_data}), 400
            else:
                return jsonify({'result': 'Tệp không hợp lệ'}), 400
    else: 
        return jsonify({'result': 'File is invalid, only accept .xlsx, .xls, .csv'}), 400

            

# API download file
@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    # Kiểm tra xem file có tồn tại trong thư mục UPLOAD_FOLDER không
    if os.path.isfile(os.path.join(app.config['DOWNLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return jsonify({'result': 'File not found'}), 404


""" DELETE """
""" PUT """
""" PATCH """

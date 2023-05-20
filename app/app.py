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

# TEST API
""" GET """
@app.route('/api/data/<string:object>', methods=['GET'])
def get_list_data_object_from_db(object):
    if object == 'courses':
        data = get_list_data('courses')
    elif object == 'rooms':
        data = get_list_data('rooms')
    elif object == 'timelessons':
        data = get_list_data('timelessons')
    else:
        return jsonify({'result': 'Không tìm thấy dữ liệu'}), 404
    return jsonify({'result': data}), 200

# API get list of schedule best fitness from database
from db.service import get_list_classes_by_schedule_best


@app.route('/api/schedule', methods=['GET'])
def get_schedules():
    schedule = []
    for i in range(0, len(get_list_classes_by_schedule_best())):
        schedule.append({
            'maHocPhan': get_list_classes_by_schedule_best()[i][0],
            'tenHocPhan': get_list_classes_by_schedule_best()[i][1],
            'tenLopHoc': get_list_classes_by_schedule_best()[i][2],
            'tenGiangVien': get_list_classes_by_schedule_best()[i][3],
            'tenPhongHoc': get_list_classes_by_schedule_best()[i][4],
            'thoiGianHoc': get_list_classes_by_schedule_best()[i][5],
            'soLuongSinhVien': get_list_classes_by_schedule_best()[i][6],
            'sucChua': get_list_classes_by_schedule_best()[i][7],
        })
    return jsonify({'result': schedule}), 200

# API start GA algorithm
#@app.route('/api/start-ga', methods['POST'])
# GA Module support
import time

from prettytable import PrettyTable

from ga.ga import GA
from ga.population import Population
from utils.display_prettytable import display_result
from utils.sound_notification import sound_notification

from ga.course import init_courses
from ga.room import init_rooms
from ga.timelesson import init_timelessons

global info_ga
info_ga = courses_per_resource(get_all_courses('courses'), get_list_data('rooms'), get_list_data('timelessons'))
global course_db, room_db, timelesson_db

@app.route('/api/ga/start', methods=['GET'])
def run_genetic_algorithm():
    # Kiểm tra điều kiện dữ liệu đầu vào
    courses_db = get_all_courses('courses')
    rooms_db = get_list_data('rooms')
    timelessons_db = get_list_data('timelessons')
    if len(courses_db) == 0:
        result_check = False, "Bạn chưa import dữ liệu lớp học phần (COURSES)"
    elif len(rooms_db) == 0:
        result_check = False, "Bạn chưa import dữ liệu phòng học (ROOMS)"
    elif len(timelessons_db) == 0:
        result_check = False, "Bạn chưa import dữ liệu thời gian học (TIMELESSONS)"
    elif len(courses_db) > (len(rooms_db) * len(timelessons_db)):
        result_check = False, "[Số lượng lớp học phần (COURSES)] > [số lượng phòng học (ROOMS)] x [số lượng thời gian học (TIMELESSONS)]"
    else:
        result_check = True, "Dữ liệu đầu vào hợp lệ"
        
    is_passed, message = result_check
    course_converted = init_courses(courses_db)
    room_converted = init_rooms(rooms_db)
    timelesson_converted = init_timelessons(timelessons_db)
    
    if is_passed == False:
        return jsonify({'result': 'Dữ liệu không hợp lệ', 'message': message}), 400
    else:
        # Lấy các thông số chạy GA từ yêu cầu POST
        #data = request.get_json()
        best_fitness = 0
        # xác định dân số ban đầu của quần thể
        population_size = 15
    
        # xác định số thế hệ (lần lặp lại) thuật toán
        num_generations = 20000
        # Tỉ lệ đột biến
        mutation_rate = 0.1 # 0.01 - 0.1
        # Tỉ lệ lai ghép
        crossover_rate = 0.85  # 0.6 - 0.9
        elitism_rate = 0.1 # 0.05 - 0.1

        # Tạo quần thể ban đầu
         # Bắt đầu tính thời gian chạy thuật toán
        start_time = time.time()
        
        population = Population(population_size, course_converted, room_converted, timelesson_converted).get_schedules()
        print("Cá thể tốt nhất trong quần thể ban đầu:")
        print(display_result(population))
    
        ga = GA(population, mutation_rate, crossover_rate, elitism_rate, course_converted, room_converted, timelesson_converted)
    
        population_result = ga.run(num_generations, start_time)
        end_time = time.time()
        running_time = end_time - start_time
        unchanged_conflict_count = ga.get_unchanged_count()
        if ga.get_is_done() == True:
            # Âm thanh thông báo hoàn thành trong 1s
            sound_notification()
            # Tắt sau 1s
            time.sleep(1)
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
        
        print("Running time: ", running_time)
        #sound_notification()
        population_result.sort(key=lambda x: x.get_fitness(), reverse=True)
        print('Best schedule fitness: ', population_result[0].get_fitness())
        display_result(population_result)
        # Lưu những kết quả tốt nhất vào database
        # Lưu schedule vào database
        # Lấy những thông tin cần lưu
        
        min_conflict = population_result[0].get_conflict()

        # Lưu các lịch có fitness bằng best_fitness
        for i in range(0, len(population_result)):
            if population_result[i].get_conflict() == min_conflict:
                # Lưu schedule vào database
                conflict = population_result[i].get_conflict()
                fitness = population_result[i].get_fitness()
                create_new_schedule(fitness, running_time, population_size, mutation_rate, crossover_rate, conflict)
                schedule_id = get_schedule_id_newest()
                for j in range(0, len(population_result[i].get_classes())):
                    course_id = population_result[i].get_classes()[j].get_course().get_course_id()
                    room_id = population_result[i].get_classes()[j].get_room().get_room_id()
                    timelesson_id = population_result[i].get_classes()[j].get_timelesson().get_timelesson_id()
                    create_classes(course_id, room_id, timelesson_id, schedule_id)

        if get_list_classes_by_schedule_id(schedule_id) == []:
            delete_schedule_by_id(schedule_id)
    return jsonify({'result': 'success'}), 200
    
# API get index input of GA: population size, mutation rate, crossover rate
@app.route('/api/ga/result-analysis', methods=['GET'])
def get_result_analysis():
    result = get_list_schedules_create_nearly()
    list_schedule = []
    for i in range(0, len(result)):
        list_schedule.append({ 
                'schedule_id': result[i][0], 
                'fitness': result[i][1],
                'confict': result[i][6],
                'created_at': result[i][7]
        })
    return jsonify({'result': 'success', 'populationSize': result[1][3], 'mutationRate': result[1][4],'crossOver': result[1][5], 'runningTime': result[1][2] , 'data': list_schedule}), 200


# API get schedule by id
@app.route('/api/schedule/<int:schedule_id>', methods=['GET'])
def get_schedule_by_id_func(schedule_id):
    schedule = []
    for i in range(0, len( get_list_classes_by_schedule_id(schedule_id))):
        schedule.append({
            'maHocPhan':  get_list_classes_by_schedule_id(schedule_id)[i][0],
            'tenHocPhan':  get_list_classes_by_schedule_id(schedule_id)[i][1],
            'tenLopHoc':  get_list_classes_by_schedule_id(schedule_id)[i][2],
            'tenGiangVien':  get_list_classes_by_schedule_id(schedule_id)[i][3],
            'tenPhongHoc':  get_list_classes_by_schedule_id(schedule_id)[i][4],
            'thoiGianHoc':  get_list_classes_by_schedule_id(schedule_id)[i][5],
            'soLuongSinhVien':  get_list_classes_by_schedule_id(schedule_id)[i][6],
            'sucChua':  get_list_classes_by_schedule_id(schedule_id)[i][7],
        })
    return jsonify({'result': schedule}), 200

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
            courses_db = get_all_courses('courses')
            rooms_db = get_list_data('rooms')
            timelessons_db = get_list_data('timelessons')
            info_ga = courses_per_resource(get_all_courses('courses'), get_list_data('rooms'), get_list_data('timelessons'))
            return jsonify({'result': 'Tệp đã tải lên thành công với tên: ' + unique_filename, 'info_ga': info_ga}), 200
        else: 
            if error_data is not None:
                return jsonify({'result': error_data}), 400
            else:
                return jsonify({'result': 'Tệp không hợp lệ'}), 400
    else: 
        return jsonify({'result': 'File is invalid, only accept .xlsx, .xls, .csv'}), 400

# API export file excel
from excel.write_excel import export_to_excel
#add_dataframe_to_excel('output.xlsx', ['conflict'], list_conflict, 'Conflict3')
#add_dataframe_to_excel('output.xlsx', ['Generation'], list_gene, 'Generation3')
from datetime import datetime as dt

@app.route('/api/export/schedule', methods=['GET'])
def export_file():
    result = get_list_classes_for_export_schedule_best()
    columns = ['Mã_lớp_học_phần', 'Mã_lớp_học', 'Mã_giảng_viên', 'Tên_giảng_viên',
               'Mã_môn_học', 'Tên_môn_học', 'Số_lượng_sinh_viên', 'Tên_phòng_học',
               'Sức_chứa', 'Loại_phòng', 'Mã_UUID', 'Thời_gian_học']

    df = pd.DataFrame(result, columns=columns)

    # Tạo tên file tự động dựa trên thời gian
    current_time = dt.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"schedule_fitness_{current_time}.xlsx"

    # Tạo đường dẫn cho file xuất
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], file_name)

    # Xuất DataFrame thành file Excel
    df.to_excel(file_path, index=False)

    # Kiểm tra xem file có tồn tại hay không
    if os.path.isfile(file_path):
        # Trả về đường dẫn của file để người dùng tải xuống
        return jsonify({'file_url': file_path})
    else:
        return jsonify({'result': 'File not found'}), 404

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

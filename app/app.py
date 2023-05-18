from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# IMPORT DB SERVICE
from db.service import *

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

from ga.ga import GA
from ga.population import Population
from utils.display_prettytable import display_result
from utils.sound_notification import sound_notification
from prettytable import PrettyTable

# TEST API
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'result': 'success'}), 200

# API khởi chạy GA
#@app.route('/api/start-ga', methods['POST'])
@app.route('/api/start-ga', methods=['GET'])
def run_genetic_algorithm():
    # Lấy các thông số chạy GA từ yêu cầu POST
    #data = request.get_json()
    best_fitness = 0
    # xác định dân số ban đầu của quần thể
    population_size = 80
    
    # xác định số thế hệ (lần lặp lại) thuật toán
    num_generations = 20000
    # Tỉ lệ đột biến
    mutation_rate = 0.1 # 0.01 - 0.1
    # Tỉ lệ lai ghép
    crossover_rate = 0.85  # 0.6 - 0.9
    elitism_rate = 0.1 # 0.05 - 0.1
    
    # Tạo quần thể ban đầu
    start_time = time.time()
    population = Population(population_size).get_schedules()
    print("Cá thể tốt nhất trong quần thể ban đầu:")
    print(display_result(population))
    
    ga = GA(population, mutation_rate, crossover_rate, elitism_rate)
    
    population_result = ga.run(num_generations)
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
    end_time = time.time()
    print("Time: ", end_time - start_time)
    if ga.get_population()[0].get_conflict() == 0 :
        sound_notification()
        population_result.sort(key=lambda x: x.get_fitness(), reverse=True)
        print('Best schedule fitness: ', population_result[0].get_fitness())
        display_result(population_result)
        # Lưu những kết quả tốt nhất vào database
        # Lưu schedule vào database
        # Lấy những thông tin cần lưu
        fitness = population_result[0].get_fitness()
        running_time = end_time - start_time
        
        create_new_schedule(fitness, running_time, population_size, mutation_rate, crossover_rate)
        schedule_id = get_schedule_id_newest()
        # Lưu classes vào database
        for i in range(0, len(population_result[0].get_classes())):
            course_id = population_result[0].get_classes()[i].get_course().get_course_id()
            room_id = population_result[0].get_classes()[i].get_room().get_room_id()
            timelesson_id = population_result[0].get_classes()[i].get_timelesson().get_timelesson_id()
            print(course_id, room_id, timelesson_id, schedule_id)
            create_classes(course_id, room_id, timelesson_id, schedule_id)
        # Nếu các classes không lưu vào db, xóa schedule vừa lưu
        if get_list_classes_by_schedule_id(schedule_id) == []:
            delete_schedule_by_id(schedule_id)
        return jsonify({'result': 'success'}), 200

# API get list of schedule best fitness from database
from db.service import get_list_classes_by_schedule_id_newest

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    result = get_list_classes_by_schedule_id_newest()
    print(result)
    schedule = []
    for i in range(0, len(result)):
        schedule.append({
            'maHocPhan': result[i][0],
            'tenHocPhan': result[i][1],
            'tenLopHoc': result[i][2],
            'tenGiangVien': result[i][3],
            'tenPhongHoc': result[i][4],
            'thoiGianHoc': result[i][5],
        })
    return jsonify({'result': schedule}), 200


from app.app import Flask, request, jsonify

app = Flask(__name__)

# GA Module support
import time

from ga.ga import GA
from ga.population import Population
from utils.display_prettytable import display_result
from utils.sound_notification import sound_notification
from db.service import get_all_courses

# API khởi chạy GA
#@app.route('/api/start-ga', methods['POST'])
@app.route('/api/start-ga', methods['GET'])
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
    display_result(population)
    
    ga = GA(population, mutation_rate, crossover_rate, elitism_rate)
    
    pop_result = ga.run(num_generations)
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
        pop_result.sort(key=lambda x: x.get_fitness(), reverse=True)
        print('Best schedule fitness: ', pop_result[0].get_fitness())
        display_result(pop_result)
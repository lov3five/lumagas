import os
import sys
import pandas as pd
# Lấy đường dẫn gốc của dự án
project_root = os.path.dirname(os.path.abspath(__file__))
# Thêm đường dẫn gốc vào PYTHONPATH
sys.path.append(project_root)

from db.service import get_list_data

# IMPORT FLASK APP
from app.app import app

# GA
from ga.ga import GA
from ga.population import Population
from utils import sound_notification, display_prettytable
import time

from prettytable import PrettyTable
def main():
    best_fitness = 0
    
    population_size = 80
    
    num_generations = 10000
    
    crossover_rate = 0.85 
    
    mutation_rate = 0.1 # 0.01 - 0.1
    
    elitism_rate = 0.1 






if __name__ == '__main__':
    app.run()
    #

from db import timelessons_db
from db import rooms_db
from db import courses_db

from ga.course import init_courses
from ga.room import init_rooms
from ga.timelesson import init_timelessons
from ga.schedule import Schedule

courses = init_courses(courses_db)
rooms = init_rooms(rooms_db)
timelessons = init_timelessons(timelessons_db)

class Population:
    def __init__(self, population_size):
        self.population_size = population_size
        self.schedules = [Schedule(courses, rooms, timelessons).init_schedule() for _ in range(population_size)]
        self.fittest = None
        
    def get_schedules(self):
        return self.schedules
    
    def get_fittest(self):
        return self.fittest

    def set_fittest(self, fittest):
        self.fittest = fittest
        
    def get_population_size(self):
        return self.population_size
    




from ga.schedule import Schedule

class Population:
    def __init__(self, population_size, courses, rooms, timelessons):
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
    




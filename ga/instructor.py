class Instructor:
    def __init__(self, instructor_id, instructor_name, max_courses):
        self.instructor_id = instructor_id
        self.instructor_name = instructor_name
        self.max_courses = max_courses
        
    def get_instructor_id(self):
        return self.instructor_id
    
    def set_instructor_id(self, instructor_id):
        self.instructor_id = instructor_id
    
    def get_instructor_name(self):
        return self.instructor_name
    
    def set_instructor_name(self, instructor_name):
        self.instructor_name = instructor_name
        
    def get_max_courses(self):
        return self.max_courses
    
    def set_max_courses(self, max_courses):
        self.max_courses = max_courses
    
    def __str__(self):
        return f"Instructor: {self.instructor_id} | {self.instructor_name} | {self.max_courses}"
class Course:
    def __init__(self, course_id, classroom_id, instructor_id, instructor_name, subject_id, subject_name, max_students):
        self.course_id = course_id
        self.max_students = max_students
        self.instructor_id = instructor_id
        self.instructor_name = instructor_name
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.classroom_id = classroom_id
        
        
    def get_course_id(self):
        return self.course_id
    
    def set_course_id(self, course_id):
        self.course_id = course_id
    
    def get_max_students(self):
        return self.max_students
    
    def set_max_students(self, max_students):
        self.max_students = max_students
    
    def get_instructor_id(self):
        return self.instructor_id
    
    def set_instructor_id(self, instructor_id):
        self.instructor_id = instructor_id
    
    def get_instructor_name(self):
        return self.instructor_name
    
    def set_instructor_name(self, instructor_name):
        self.instructor_name = instructor_name
        
    def get_subject_id(self):
        return self.subject_id
    
    def set_subject_id(self, subject_id):
        self.subject_id = subject_id
    
    def get_subject_name(self):
        return self.subject_name
    
    def set_subject_name(self, subject_name):
        self.subject_name = subject_name
        
    def get_classroom_id(self):
        return self.classroom_id
    
    def set_classroom_id(self, classroom_id):
        self.classroom_id = classroom_id
    
    def __str__(self):
        return "Course: " + self.course_id + " | " + "Instructor: " + self.instructor_name + " | " + "Subject: " + self.subject_name + " | " + "Classroom: " + self.classroom_id


# Hàm khởi tạo danh sách các khóa học
def init_courses(courses_db):
    courses = []
    for course in courses_db:
        courses.append(Course(course[0], course[1], course[2], course[3], course[4], course[5], course[6]))
    return courses

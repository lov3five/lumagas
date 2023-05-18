from prettytable import PrettyTable

def display_result(data):
    x = PrettyTable()
    x.field_names = ["Classes(id)", "Môn học(id)", "Lớp học phần", "Room(capacity)", "Giảng viên", "Thời gian"]
    for i in range(len(data[0].get_classes())):
      x.add_row([data[0].get_classes()[i].get_id(), data[0].get_classes()[i].get_course().get_subject_name(),data[0].get_classes()[i].get_course().get_course_id(), data[0].get_classes()[i].get_room(), data[0].get_classes()[i].get_course().get_instructor_name(), data[0].get_classes()[i].get_timelesson()])
    print(x)
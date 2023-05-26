from prettytable import PrettyTable

def display_result(data):
    x = PrettyTable()
    x.field_names = ["ID", "Môn học", "Lớp học phần", "Phòng học", "Sức chứa", "Giảng viên", "Thời gian học"]
    for i in range(len(data[0].get_classes())):
      x.add_row([data[0].get_classes()[i].get_id(), data[0].get_classes()[i].get_course().get_subject_name(),data[0].get_classes()[i].get_course().get_classroom_id(), data[0].get_classes()[i].get_room().get_room_name(), data[0].get_classes()[i].get_course().get_instructor_name(), data[0].get_classes()[i].get_room().get_room_capacity(), data[0].get_classes()[i].get_timelesson().get_timelesson_period()])
    return x
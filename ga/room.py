class Room:
    def __init__(self,id , name, capacity, type):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.type = type

    def get_room_id(self):
        return self.id
    
    def get_room_name(self):
        return self.name
    
    def get_room_capacity(self):
        return self.capacity
    
    def get_room_type(self):
        return self.type
    
    def __str__(self):
        return f'Room: {self.name} - Capacity: {self.capacity} - Type: {self.type}'

def init_rooms(rooms_db):
    rooms = []
    for room in rooms_db:
        rooms.append(Room(room[0], room[1], room[2], room[3]))
    return rooms



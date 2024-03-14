# Activity Class

class Activity:

    # Constructor method to initialize attributes
    def __init__(self, name, instructor, date, time_length, capacity, plan_type, enabled, ident=None):
        self.name = name
        self.instructor = instructor
        self.date = date
        self.time_length = time_length
        self.capacity = capacity
        self.plan_type = plan_type
        self.enabled = enabled
        self.ident = ident

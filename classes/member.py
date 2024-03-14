# Member Class

class Member:

    # Constructor method to initialize attributes
    def __init__(self, name, surname, birth_day, address, phone, email, plan_type, start_date, enabled, img,
                 ident=None):
        self.name = name
        self.surname = surname
        self.birth_day = birth_day
        self.address = address
        self.phone = phone
        self.email = email
        self.plan_type = plan_type
        self.start_date = start_date
        self.enabled = enabled
        self.ident = ident
        self.img = img

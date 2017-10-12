class Education:
    global university, major, degree, gpa, year, street, city, state, country, zipcode

    def __init__(self):
        self.university = ""
        self.major = ""
        self.degree = ""
        self.gpa = ""
        self.year = ""
        self.city = ""
        self.state = ""
        self.country = "USA"
        self.zipcode = ""

    def set_university(self, university):
        self.university = university

    def set_major(self, major):
        self.major = major

    def set_degree(self, degree):
        self.degree = degree

    def gpa(self, gpa):
        self.gpa = gpa

    def set_year(self, year):
        self.year = year

    def set_addr(self, street=None, city=None, state=None, country=None, zipcode=None):
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode

    def get_university_name(self):
        return self.university

    def get_major(self):
        return self.major

    def get_degree(self):
        return self.degree

    def get_gpa(self):
        return self.gpa

    def get_year(self):
        return self.year

    def get_street(self):
        return self.street

    def get_city(self):
        return self.city

    def get_state(self):
        return self.street

    def get_country(self):
        return country

    def get_zipcode(self):
        return self.zipcode

    def display(self):
        print "Education Detail:"
        print "University / College / High School: ", self.university
        print "Degree: ", self.degree
        print "Major: ", self.major
        print "GPA: ", self.gpa
        print "Year:", self.year
        # print "Street: ",self.street
        print "City: ", self.city, " State: ",self.state, " Country: ", self.country, " zipcode: ", self.zipcode
        print ""
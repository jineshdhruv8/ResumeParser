class Company:
    global name, year, description, position, street, city, state, country, zipcode

    def __init__(self):
        self.name = ""
        self.year = ""
        self.description = ""
        self.position = ""
        self.city = ""
        self.state = ""
        self.country = ""
        self.zipcode = ""

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_position(self, position):
        self.position = position

    def set_year(self, year):
        self.year = year

    def set_addr(self, street=None, city=None, state=None, country=None, zipcode=None):
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode

    def get_company_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_position(self):
        return self.position

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


class Experience:
    global exp_list

    def __init__(self):
        self.exp_list = []

    def add_experience(self, company):
        self.exp_list.append(company)

    def get_experience(self):
        return self.exp_list

    def display(self):
        for company in self.exp_list:
            print "Company Name:", company.name
            print "Position: ", company.position
            print "Year: ", company.year
            print "Description: ", company.description
            print "City: ", self.city, " State: ", self.state, " Country: ", self.country, " zipcode: ", self.zipcode
            print ""

from education_detail import Education


class User:
    global first_name, last_name, full_name, email, phone, street, city, state, country, zipcode, link, education

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.full_name = ""
        self.email = ""
        self.phone = ""
        self.street = ""
        self.city = ""
        self.state = ""
        self.country = "USA"
        self.zipcode = ""
        self.link = []
        self.education = Education()
        pass


    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_full_name(self, full_name):
        self.full_name = full_name

    def set_email(self, email):
        self.email = email

    def set_phone(self, phone):
        self.phone = phone

    def set_addr(self, street=None, city=None, state=None, country=None, zipcode=None):
        self.street = street
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode

    def set_link(self, link):
        self.link = link

    def set_edu_obj(self, education):
        self.education = education

    def get_full_name(self):
        return self.full_name

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.email

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

    def get_link(self):
        return self.link

    def get_edu_obj(self):
        return self.education

    def display(self):
        print "User Detail:"
        print "Full Name: ", self.full_name
        # print "First Name: ", self.first_name
        # print "Last Name: ", self.last_name
        print "Email: ", self.email
        print "Phone: ", self.phone
        print "Link: ", self.link
        # print "Street: ",self.street
        print "City: ", self.city, " State: ",self.state, " Country: ", self.country, " zipcode: ", self.zipcode
        print ""


def main():
    u = User()
    p = User()

    u.set_first_name("jinesh")
    p.set_first_name("raj")

    print u.first_name, p.first_name



if __name__ == '__main__':
    main()
import csv
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
import pdfminer
from bson import ObjectId
import gridfs
import unicodedata
import datefinder
import datetime

from education_detail import Education
from user_detail import User
import sys
from uszipcode import ZipcodeSearchEngine
import nltk
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

reload(sys)
sys.setdefaultencoding('utf-8')

key_file_path = "key.csv"
text_dict = {}
text_prop_dict = {}
user_id = 1

def read_PDF_Miner(fileObj):
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fileObj)

    # Create a PDF document object that stores the document structure.
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # loop over all pages in the document
    for page in PDFPage.create_pages(document):
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()
        id = 0
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBoxHorizontal):
                # print(lt_obj.__class__.__name__)
                # print(lt_obj.bbox, " ", type(lt_obj.bbox))
                # print ("Height: ", lt_obj.height, " Width: ", lt_obj.width)
                # print(
                # "Is Digit: ", lt_obj.get_text().isdigit(), "  Is Title: ", lt_obj.get_text().istitle(), "  Is Lower: ",
                # lt_obj.get_text().islower())
                # print("Is Alnum: ", lt_obj.get_text().isalnum(), "  Is Identifier: ", lt_obj.get_text().find("+"),
                #       "  Is Space: ", lt_obj.get_text().isspace())
                # print(lt_obj.get_text())
                text_dict[id] = lt_obj.get_text()
                text_prop_dict[id] = lt_obj
                id += 1

def extract_user_detail():
    top_text_id = -1
    max_val = -100000000

    """
    Extract Name: Iterate all the layout objects to get the text which is present
    at the top of the page which is the name of the person
    """
    for key, lt_obj in text_prop_dict.iteritems():
        if (lt_obj.bbox[1] > max_val and not lt_obj.get_text().isspace()):
            top_text_id = key
            max_val = lt_obj.bbox[1]

    def get_name(top_text_id):

        email_flag = False
        phone_flag = False
        link_flag = False

        name_object = text_prop_dict.get(top_text_id)
        text = name_object.get_text()
        text = str(unicodedata.normalize('NFKD', text).encode('utf-8')).strip()
        sentences = nltk.sent_tokenize(text)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        full_name = []
        # print text, sentences[0]
        for item in sentences[0]:
            # convert tuple to list
            item_list = list(item)
            # Search consecutive Proper Noun
            if 'NNP' in item_list and (item_list[0].istitle() or str(item_list[0]).isupper()):
                full_name.append(item_list[0])
            else:
                break
        # check email in name object
        index = text.find("@")
        if index > 0:
            email_flag = True

        # check phone number in name object
        cell = re.search("\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}", text)
        if cell:
            phone_flag = True
        name = " ".join(full_name)

        # check hyperlinks in name object
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        if len(urls) > 0:
            link_flag = True

        return  name, email_flag, phone_flag, link_flag

    def get_email(text):
        text = str(unicodedata.normalize('NFKD', text).encode('utf-8'))
        index = text.find("@")
        if index > 0:
            return (re.search(r'[\w\.-]+@[\w\.-]+', text)).group(0)
        else:
            for k,v in text_dict.iteritems():
                v = str(unicodedata.normalize('NFKD', v).encode('utf-8'))
                text = re.search(r'[\w\.-]+@[\w\.-]+', v)
                if text:
                    return text.group(0)
        return None

    def get_cell(text):
        text = str(unicodedata.normalize('NFKD', text).encode('utf-8'))
        cell = re.search("\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}", text)
        if cell:
            return cell.group(0)
        else:
            for k,v in text_dict.iteritems():
                v = str(unicodedata.normalize('NFKD', v).encode('utf-8'))
                cell = re.search("\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}", v)

                if cell:
                    return cell.group(0)
            return None

    def get_zipcode(text):
        text = str(unicodedata.normalize('NFKD', text).encode('utf-8'))
        zip_code = re.search(r'\b\d{5}(?:[-\s]\d{4})?\b', text)
        # print zip_code
        if zip_code:
            return zip_code.group(0)
        else:
            for k,v in text_dict.iteritems():
                v = str(unicodedata.normalize('NFKD', v).encode('utf-8'))
                zip_code = re.search(r'\b\d{5}(?:[-\s]\d{4})?\b', v)
                if zip_code:
                    return zip_code.group(0)
        return None

    def get_links(text):
        text = str(unicodedata.normalize('NFKD', text).encode('utf-8'))
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

        if len(urls) > 0:
            return urls
        else:
            result = []
            for k, v in text_dict.iteritems():
                v = str(unicodedata.normalize('NFKD', v).encode('utf-8'))
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',v)
                if len(urls) > 0:
                    result.extend(urls)
        return result

    user = User()
    neighbor = find_neighbor(top_text_id)

    full_name, email_flag, phone_flag, link_flag = get_name(top_text_id)
    user.set_full_name(full_name)

    if not email_flag and not neighbor == None:
        user.set_email(get_email(neighbor.get_text()))
    else:
        name_object = text_prop_dict.get(top_text_id)
        text = name_object.get_text()
        user.set_email(get_email(text))

    if not phone_flag and not neighbor == None:
        user.set_phone(get_cell(neighbor.get_text()))
    else:
        name_object = text_prop_dict.get(top_text_id)
        text = name_object.get_text()
        user.set_phone(get_cell(text))

    if not neighbor == None:
        zipcode = get_zipcode(neighbor.get_text())
        # Use zipcode dictionary to find state and city
        search = ZipcodeSearchEngine()
        zip_obj = search.by_zipcode(zipcode)
        state = zip_obj.State
        city = zip_obj.City
        user.set_addr(None,city, state, "USA", zipcode)

    if not link_flag and not neighbor == None:
        user.set_link(get_links(neighbor.get_text()))
    else:
        name_object = text_prop_dict.get(top_text_id)
        text = name_object.get_text()
        user.set_link(get_links(text))

    # user.display()
    # show_object(neighbor)
    return user

def find_neighbor(key):
    min_vdist, min_hdist = 1000000, 1000000
    id = 0
    neighbor = ""
    name_object = text_prop_dict.get(key)

    for k, lt_obj in text_prop_dict.iteritems():
        # print "Key: ", k, "     vdist: ", name_object.vdistance(lt_obj), "              hdist: ", name_object.hdistance(
        #     lt_obj), "            voverlap: ", name_object.voverlap(lt_obj), "     hoverlap: ", name_object.hoverlap(
        #     lt_obj)
        # print name_object.vdistance(lt_obj) <= min_vdist, name_object.hdistance(lt_obj) <= min_hdist
        # print lt_obj.get_text()
        # text = str(unicodedata.normalize('NFKD', lt_obj.get_text()).encode('utf-8'))
        # sentences = nltk.sent_tokenize(text)
        # sentences = [nltk.word_tokenize(sent) for sent in sentences]
        # sentences = [nltk.pos_tag(sent) for sent in sentences]
        # print sentences
        # print "\n\n\n"
        if (name_object.vdistance(lt_obj) + name_object.hdistance(lt_obj) <= (min_hdist + min_vdist)):
            if (not (name_object.vdistance(lt_obj) == 0 and name_object.hdistance(lt_obj) == 0)):
                text = str(unicodedata.normalize('NFKD', lt_obj.get_text()).encode('utf-8'))
                if text.__contains__("@"):
                    min_vdist = name_object.vdistance(lt_obj)
                    min_hdist = name_object.hdistance(lt_obj)
                    neighbor = lt_obj
                    id = k
    if neighbor == "":
        return None

    return neighbor

def extract_education_detail(user):
    dir_path = "/home/jinesh/Desktop/Capstone Project/Code/word_list/"

    def get_education_word_list(dir_path):
        file_name = "education_segment.csv"
        reader = read_csv(dir_path+file_name)
        education_word_list = []
        for row in reader:
            education_word_list.append(row[0])
        return education_word_list

    def get_qualification_word_list(dir_path):
        file_name = "qualification_degree_list.csv"
        reader = read_csv(dir_path+file_name)
        qualification_word_dict = {}
        abbr_list = []
        degree_list = []
        for row in reader:
            # print row
            abbr_list.append(row[0])
            degree_list.append(row[1])
            qualification_word_dict[row[0]] = row[1]
        return qualification_word_dict, abbr_list, degree_list

    def get_major_word_list(dir_path):
        file_name = "educational_major.csv"
        reader = read_csv(dir_path + file_name)
        major_list = []
        for row in reader:
            major_list.append(row[0])
        return major_list

    def get_university_word_list(dir_path):
        file_name = "university.csv"
        reader = read_csv(dir_path + file_name)
        university_word_dict = {}
        for row in reader:
            value = [row[2], row[3], row[4], row[5]]
            university_word_dict[row[1]] = value
        return  university_word_dict

    def search_major(text, degree, edu_obj):

        degree_flag = False
        max = -1
        # Search for major
        for major in major_word_list:
            # print major
            if major.lower() in (text.lower()) and len(major) > max:
                edu_obj.major = str(major).title()
                edu_obj.degree = degree.title()
                max = len(str(major))
                degree_flag = True

        # print "computer science" in text.lower()

        return degree_flag

    def search_date(text, edu_obj):
        # Search for Date
        matches = list(datefinder.find_dates(text))
        edu_date = ""
        for temp_date in matches:
            edu_date += str(temp_date.month) + "/" + str(temp_date.year) + " - "
        edu_obj.year = edu_date[:(len(edu_date) - 2)]

    def get_shortlisted_keys(education_word_list, qualification_word_dict, university_word_dict,major_word_list):

        edu_obj = Education()
        user.set_edu_obj(edu_obj)
        degree_list = ['associate','bachelor','bachelor\'s','masters', 'master', 'master\'s', 'doctoral']
        text_list = []
        for k, lt_obj in text_prop_dict.iteritems():
            text = str(unicodedata.normalize('NFKD', lt_obj.get_text()).encode('utf-8'))
            flag = True

            # Search Education keyword
            for word in education_word_list:
                if word in text.lower():

                    # print  "Graduation" in text

                    # Search for university
                    for university, addr_list in university_word_dict.iteritems():
                        if str(university).lower() in text.lower():
                            # print university,text.lower().find(university.lower()), 'Date: ', text.lower().find()

                            edu_obj.university = university
                            edu_obj.set_addr(addr_list[0], addr_list[1], addr_list[2], "USA", addr_list[3])
                            degree_flag = False

                            # Search for degree
                            for degree in degree_list:
                                if degree.lower() in text.lower():
                                    degree_flag = search_major(text, degree, edu_obj)

                            # Search for degree if not found earlier
                            if not degree_flag:
                                search_major(text, degree, edu_obj)
                                for key, val in qualification_word_dict.iteritems():
                                    if key in text:
                                        edu_obj.degree = val
                                    if val in text and edu_obj.major == "":
                                        edu_obj.major =  val

                            search_date(text, edu_obj)
                    break
        user.display()
        edu_obj.display()

    education_word_list = get_education_word_list(dir_path)
    qualification_word_dict, abbr_list, degree_list = get_qualification_word_list(dir_path)
    university_word_dict = get_university_word_list(dir_path)
    major_word_list = get_major_word_list(dir_path)
    get_shortlisted_keys(education_word_list, qualification_word_dict, university_word_dict,major_word_list)


def display_list(obj_list):
    for lt_obj in obj_list:
        print lt_obj.__class__.__name__
        print(lt_obj.bbox, " ", type(lt_obj.bbox))
        print ("Height: ", lt_obj.height, " Width: ", lt_obj.width)
        print("Is Digit: ", lt_obj.get_text().isdigit(), "  Is Title: ", lt_obj.get_text().istitle(), "  Is Lower: ",
              lt_obj.get_text().islower())
        print(
            "Is Alnum: ", lt_obj.get_text().isalnum(), "  Is Identifier: ", lt_obj.get_text().find("+"), "  Is Space: ",
            lt_obj.get_text().isspace())
        print lt_obj.get_text()


def display():
    for k, v in text_dict.iteritems():
        lt_obj = text_prop_dict.get(k)

        print "Key : ", k, "  ", lt_obj.__class__.__name__
        print(lt_obj.bbox, " ", type(lt_obj.bbox))
        print ("Height: ", lt_obj.height, " Width: ", lt_obj.width)
        print("Is Digit: ", lt_obj.get_text().isdigit(), "  Is Title: ", lt_obj.get_text().istitle(), "  Is Lower: ",
              lt_obj.get_text().islower())
        print(
        "Is Alnum: ", lt_obj.get_text().isalnum(), "  Is Identifier: ", lt_obj.get_text().find("+"), "  Is Space: ",
        lt_obj.get_text().isspace())
        print v


def show_object(lt_obj):
    print lt_obj.__class__.__name__
    print(lt_obj.bbox)
    print ("Height: ", lt_obj.height, " Width: ", lt_obj.width)
    print("Is Digit: ", lt_obj.get_text().isdigit(), "  Is Title: ", lt_obj.get_text().istitle(), "  Is Lower: ",
          lt_obj.get_text().islower())
    print(
        "Is Alnum: ", lt_obj.get_text().isalnum(), "  Is Identifier: ", lt_obj.get_text().find("+"), "  Is Space: ",
        lt_obj.get_text().isspace())
    print lt_obj.get_text()


def parse_resume(key):
    con = connect_db()
    db = con.meteor
    fs = gridfs.GridFS(db)
    obj = fs.get(ObjectId(key))
    read_PDF_Miner(obj)
    user = extract_user_detail()
    extract_education_detail(user)


def insert_file(dir_path, con, pdf_file_list):
    global key_file_path, user_id

    db = con.meteor
    db['user_id_mapping'].drop()
    user_id_collection = db['user_id_mapping']

    user_id_obj_dict = {}
    user_id_pdf_dict = {}

    for pdf in pdf_file_list:
        file_path = dir_path + pdf
        pdffileobj = open(file_path, 'rb')

        fs = gridfs.GridFS(db)
        id = fs.put(pdffileobj)
        user_id_obj_dict[str(user_id)] = str(id)
        user_id_pdf_dict[str(user_id)] = pdf
        user_id += 1

    user_id_collection.insert_many([user_id_obj_dict])

    # For local storage
    for k, v in user_id_obj_dict.iteritems():
        write_csv_file(key_file_path, [[k, v, user_id_pdf_dict.get(k)]], 'a+')


def connect_db():
    from pymongo import MongoClient
    con = MongoClient(host='127.0.0.1', port=3001)
    return con


def upload_file_dir(dir_path):
    from os import walk

    # Load all pdf files from the given directory
    pdf_files = []
    for (dirpath, dirnames, filenames) in walk(dir_path):
        for name in filenames:
            if str(name).find(".pdf") > 0:
                pdf_files.append(name)

    insert_file(dir_path,connect_db(), pdf_files)


def fetch_file_from_mongod():
    con = connect_db()
    db = con.meteor
    user_id_collection = db['user_id_mapping']

    cursor = user_id_collection.find()
    document_dict = cursor[0]
    counter = 1
    for k,v in document_dict.iteritems():

        if not k == "_id":

            if counter > 11:
                # print k, get_info(k)
                print "Resume: ", get_info(k), "\n"
                parse_resume(v)
                print "\n\n\n\n"

        if counter == 12:
            break
        counter += 1
    print "done"

def get_info(key):
    global key_file_path
    reader = read_csv(key_file_path)
    for row in reader:
        if row[0] == key:
            return row[2]


def read_csv(input_file):
    """
    This function will read the csv file
    :param input_file: Name of the file
    :return:
    """

    file = open(input_file, 'r')
    reader = csv.reader(file)
    return reader


def write_csv_file(absolute_file_path, content_list, access_type):
    """
    This function will write post or campaign level metrics to the specified file

    Usage::

        >>> write_csv_file('Absolute_File_Path',[['valid','list'],[]],'a+')

    :param absolute_file_path:  The absolute path of output file
    :param content_list:        The metric list of list
    :param access_type:         It indicates type of access(write, append, etc.)
    :return:                    None

    """
    import csv
    try:
        with open(absolute_file_path, access_type) as file:
            wr = csv.writer(file)

            for row in content_list:
                wr.writerow(row)

    except Exception as e:
        raise e


def main():
    # dir_path = "/home/jinesh/Desktop/PDF/"
    # upload_file_dir(dir_path)
    fetch_file_from_mongod()

if __name__ == '__main__':
    main()

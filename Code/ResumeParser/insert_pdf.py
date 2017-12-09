import gridfs
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
key_file_path = "key.csv"
user_id = 1


def connect_db():
    from pymongo import MongoClient
    con = MongoClient(host='127.0.0.1', port=3001)
    return con


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


def upload_file_dir(dir_path):
    from os import walk

    # Load all pdf files from the given directory
    pdf_files = []
    for (dirpath, dirnames, filenames) in walk(dir_path):
        for name in filenames:
            if str(name).find(".pdf") > 0:
                pdf_files.append(name)

    insert_file(dir_path,connect_db(), pdf_files)


def main():
    # dir_path = "/home/jinesh/Desktop/PDF/"
    dir_path = "database/"
    upload_file_dir(dir_path)


if __name__ == '__main__':
    main()

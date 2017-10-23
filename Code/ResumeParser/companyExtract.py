import json
from pprint import pprint


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
    dir_path = "/home/jinesh/Desktop/Capstone Project/Code/word_list/"
    input_file = dir_path + "companies.json"

    # Reading data back
    company_list = []
    for line in open(input_file, 'r'):
        company_list.append([json.loads(line)['_source']['name']])



    output_file = dir_path + "companies.csv"
    write_csv_file(output_file, [["Company Name"]], 'w')
    write_csv_file(output_file, company_list, 'a+')


if __name__ == '__main__':
    main()
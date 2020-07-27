import os
import sys
import re

from xml.etree import ElementTree
from zipfile import ZipFile


def bill_search(argv):
    """
    This method will unzip the Data Engineering Deliverable file and scan the XML files for a regex match.
    It will return a list of bills that match the regex.

    :param argv:  List of command line arguments.
    """
    # regex validation checking
    if len(argv) != 1:
        print('Please provide one regular expression.')
        return
    try:
        regex = re.compile(argv[0])
    except re.error:
        print('Please provide a valid regular expression.')
        return

    input_zip = 'Data Engineering Deliverable - BILLSTATUS-116-sres.zip'
    output_folder = input_zip[:-4]
    inner_folder = 'BILLSTATUS-116-sres (3)'
    bills_to_return = []

    # unzip the file
    try:
        with ZipFile(input_zip, 'r') as zip_file:
            zip_file.extractall(output_folder)
    except Exception as zip_exception:
        print(f'Exception while unzipping: {zip_exception}')

    try:
        for file_path in os.scandir(f'{output_folder}/{inner_folder}'):
            if file_path.path.lower().endswith('.xml'):
                xml_tree = ElementTree.parse(file_path.path)
                root_node = xml_tree.getroot()
                # if the billSummaries text does not exist, continue past this XML file
                if root_node.find('.//billSummaries').text is None:
                    continue
                if regex.search(root_node.find('.//billSummaries//text').text):
                    bills_to_return.append(
                        f"{root_node.find('.//billType').text} {root_node.find('.//billNumber').text}")

    except Exception as search_exception:
        print(f'Exception while searching: {search_exception}')

    print('Found the following bills:')
    for bill in bills_to_return:
        print(bill)


if __name__ == "__main__":
    bill_search(sys.argv[1:])

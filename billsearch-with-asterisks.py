import os
import sys
import re

from xml.etree import ElementTree
from zipfile import ZipFile


def bill_search_asterisk(regular_expression):
    """
    This method will unzip the Data Engineering Deliverable file and scan the XML files for a regex match.
    It will return a list of bills that match the regex along with the text summary it contains. The matching
    regex will be surrounded by asterisks.

    :param regular_expression:  A regular expression.
    """
    # regex validation checking
    try:
        regex = re.compile(regular_expression)
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

    # parse the XML files for the regular expression
    try:
        for file_path in os.scandir(f'{output_folder}/{inner_folder}'):
            if file_path.path.lower().endswith('.xml'):
                xml_tree = ElementTree.parse(file_path.path)
                root_node = xml_tree.getroot()
                # if the billSummaries text does not exist, continue past this XML file
                if root_node.find('.//billSummaries').text is None:
                    continue
                bill_summary_text = root_node.find('.//billSummaries//text').text
                if regex.search(bill_summary_text):
                    # parse the bill_summary_text to remove the <p> tags
                    parsed_text = ElementTree.fromstring(bill_summary_text).text
                    bill_string = f"{root_node.find('.//billType').text} {root_node.find('.//billNumber').text}: "

                    # use the tuple provided by match.span() to find the endpoints of the matched regex
                    # increment the remaining tuples by 2 to account for the added asterisks
                    matches_replaced = 0
                    for match in regex.finditer(parsed_text):
                        index1 = match.span()[0] + matches_replaced
                        index2 = match.span()[1] + matches_replaced
                        parsed_text = f'{parsed_text[:index1]}*{parsed_text[index1:index2]}*{parsed_text[index2:]}'
                        matches_replaced += 2
                    bills_to_return.append(f'{bill_string}{parsed_text}')

    except Exception as search_exception:
        print(f'Exception while searching: {search_exception}')

    print('Found the following bills:')
    for bill in bills_to_return:
        print(bill)


if __name__ == "__main__":
    bill_search_asterisk(sys.argv[1])

from openpyxl import Workbook
import pandas as pd
import time
import logging
from datetime import datetime
from urllib.request import urlretrieve
import os
import re
from dateutil.relativedelta import relativedelta
log = logging.getLogger('robotlog')

def download_image(url, image_name):
    log.info("download_image execution started")
    if not os.path.exists('output'):
        os.makedirs('output')
    image_path = os.path.join('output', image_name)
    urlretrieve(url, image_path)
    log.info("download_image execution ended")


def get_occurrences(text, search_phrase):
    return text.lower().count(search_phrase.lower())


def write_data_to_excel(data):
    log.info("write_data_to_excel execution started")
    headers = ['Title', 'Date', 'Description', 'Picture filename', 'Search phrases count',
               'Title or description contains currency']
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, 'output.xlsx')
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)
    log.info("write_data_to_excel execution ended, excel created at: "+ output_path)


def compare_dates(intnumber, date):
    log.info("compare_dates execution started")
    date_format = "%B %d, %Y"
    current_date = datetime.now().date()
    #print('current date = '+ str(current_date))
    #change current date format to be the same as the one taken from LATimes
    datetime.strptime(str(current_date), '%Y-%m-%d').strftime(date_format)
    if "minutes" not in date or "hours" not in date or "hour" not in date or "seconds" not in date:
        pass
    else:
        date = date.now()
    if intnumber == 1 or intnumber == 0:
        final_date_to_search = current_date - relativedelta(months=1)
    else:
        final_date_to_search = current_date - relativedelta(months=intnumber)
    #gets the Month of the date i want to extract
    final_date_to_search = final_date_to_search.strftime('%B')
    if final_date_to_search in date:
        log.info("compare_dates execution ended")
        return True
    else:
        log.info("compare_dates execution ended")
        return False

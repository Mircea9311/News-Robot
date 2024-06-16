from selenium import webdriver
import time
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from urllib.request import urlretrieve
#from openpyxl import Workbook
#import pandas as pd
import os
import re
from dateutil.relativedelta import relativedelta
import lib
import sys
log = logging.getLogger('robotlog')


def main(search_phrase, number_of_months):

    logging.basicConfig(filename='robotlogs.log', level=logging.INFO)
    log.info('Started execution')
    stop_extracting = False
    data = []
    url='https://www.latimes.com'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    wait = WebDriverWait(driver, 5)

    log.info('LATimes accessed!')
    print('LA Times accessed!')
    #click search icon to reveal the field
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/ps-header/header/div[2]/button'))).click()
    time.sleep(0.2)
    #insert search phrase into search field
    wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/ps-header/header/div[2]/div[2]/form/label/input'))).send_keys(search_phrase)
    #click search
    driver.find_element(By.XPATH, '/html/body/ps-header/header/div[2]/div[2]/form/button').click()
    log.info('Search completed!')
    #wait for the filter element to appear and change it to NEWEST
    wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='s']/option[text()='Newest']"))).click()
    #wait for newest to be located so the robot won't go crazy
    wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='s']/option[text()='Newest']")))
    log.info('Filtered news by newest')
    time.sleep(1)
    while stop_extracting == False:
        # get full article wrapper to decompose and get info later
        articles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'promo-wrapper')))
        log.info('Extracted all articles from page(10), starting decomposing...')

        for article in articles:
            row = {}
            #decompose the wrapper to get the text of the article title
            article_titles = article.find_element(By.TAG_NAME, 'h3')
            article_title = article_titles.find_element(By.TAG_NAME, 'a').text

            # get article date
            article_timestamp = article.find_element(By.CLASS_NAME, 'promo-timestamp').text
            #determine if we stop extracting
            stop_extracting = lib.compare_dates(number_of_months, article_timestamp)
            #check if we continue extracting or not
            if stop_extracting:
                print('Article timestamp = '+ article_timestamp)
                log.info("Extraction reached the desired date, exiting...")
                break
            else:
                # add title to row
                print('Extracted article with title: ' + article_title)
                log.info("Starting extacting article with title: "+ article_title)
                row['Title'] = article_title
                # add timestamp to row
                row['Date'] = article_timestamp
                log.info("Article's date extracted")

            # get description
            try:
                article_description = article.find_element(By.CLASS_NAME, 'promo-description').text
            except:
                article_description = 'No description available'
            row['Description'] = article_description
            log.info("Article's description extracted")

            # get the image source, since there are multiple sources,
            # for multiple resolutions, make the necessary splits to get the image name (part later used for download)
            article_image_filename = article.find_element(By.CLASS_NAME, 'image').get_attribute('srcset')
            link = article_image_filename.split(" ")[-2]
            unfiltered_filename = link.split("/")[-1]
            image_name = unfiltered_filename.split("%2F")[-1]
            #some images do not have the proper extension, we can add the jpg or png (probably jpg in this case)
            #but this time we replace the image with image unavailable
            if '.jpg' in image_name:
                row['Picture filename'] = image_name
            else:
                row['Picture filename'] = 'Image unavailable'
            log.info("Article's image name extracted")

            # count if title and description has the search phrase in it
            # and add them together to show the number of occurences
            search_phrase_count = (lib.get_occurrences(article_title, search_phrase)
                                   + lib.get_occurrences(article_description, search_phrase))
            row['Search phrases count'] = search_phrase_count
            log.info("Article's search phrases occurences calculated")

            #check if title or description contains currency
            if '$' in article_title or 'dollar' in article_title or 'USD' in article_title:
                contains_currency = True
            elif '$' in article_description or 'dollar' in article_description or 'USD' in article_description:
                contains_currency = True
            else:
                contains_currency = False
            row['Title or description contains currency'] = contains_currency
            log.info("Checked if article title or description contains currency")

            #find and download images, splits the link to get the highest resolution image
            high_resolution_photo_link = link.split(",")[1]
            lib.download_image(high_resolution_photo_link, image_name)
            log.info("Article's image downloaded to output folder")

            #append row
            data.append(row)

        #click next page
        driver.find_element(By.CLASS_NAME,'search-results-module-next-page').click()
        time.sleep(0.5)
        log.info("Going to next page...")

    lib.write_data_to_excel(data)
    log.info('Execution finished successfully!')

search_phrase = str(sys.argv[1])
number_of_months = int(sys.argv[2])
main(search_phrase,number_of_months)
print('Done!')
#time.sleep(30)


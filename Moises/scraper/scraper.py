import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import re
from bs4 import BeautifulSoup

nih = 'https://www.ncbi.nlm.nih.gov'
term = ['covid vaccine', 'covid treatment', 'covid symptoms', 'covid sickness']


def process_links(links):
    output = []

    # Access every link and extract content
    for element in links:
        title = element['title']
        page = requests.get(element['link'], headers={'User-Agent': 'Mozilla/5.0'})
        time.sleep(0.25)
        soup = BeautifulSoup(page.content, 'html.parser')

        xml = soup.contents
        try:
            list_temp = [title, element['link'], xml]
            output.append(list_temp)
            print(f'The link: {element["link"]} was processed')

        except:
            print(f'The link: {element["link"]} failed!')
            continue

    return output


def soup_pubmed_scrapper(term):
    url = f"https://ncbi.nlm.nih.gov/pmc/?term={term}"

    # Browser to use selenium to click buttons
    # options = webdriver.ChromeOptions()
    # options.add_argument('--start-maximized')
    links = []
    with webdriver.Chrome() as driver:
        driver.get(url)

        # Iterate to X amount of pages
        for i in range(2):
            count = 0
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Get all links that are on the site that are not copies or pdfs
            result = soup.findAll('a', href=True)
            for element in result:
                # Prevent unverified papers from being added
                if count == 20:
                    break

                if element['href'].__contains__('/articles') \
                        and not element['href'].__contains__('pdf') and not element['href'].__contains__('classic') \
                        and element.text != '\n\n':
                    l_paper = {'title': element.text, 'link': nih + element['href']}
                    links.append(l_paper)
                    count += 1

            driver.find_element(By.XPATH, '//*[@class="active page_link next"]').click()
            time.sleep(1)

    # Print progress
    log(2)

    data = process_links(links)

    create_csv(term, data)


def create_csv(term, data):
    csv_file = f'research_{term}'
    with open(f'data/new_{csv_file}.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        header = ['Title', 'Link', 'XML']
        writer.writerow(header)
        for i in data:
            writer.writerow(i)
        print(f'Successfully created file')


def log(num):
    print('=' * 40)
    if num == 1:
        print(' ' * 11, "Starting scraper")
    elif num == 2:
        print(' ' * 5, "Data scrapped successfully")
    elif num == 3:
        print(' ' * 10, "Finished Execution")
    print('=' * 40, '\n\n')


if __name__ == "__main__":
    log(1)
    for i in term:
        soup_pubmed_scrapper(i)
        break
    log(3)

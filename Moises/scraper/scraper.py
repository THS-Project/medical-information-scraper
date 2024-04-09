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


def pubmed_scrapper(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    with webdriver.Chrome(options= options) as driver:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="abstract-a.adk.b.ad"]/div[2]')))
        title = driver.find_element(By.XPATH, '//*[@id="ui-ncbiinpagenav-1"]/div[1]/h1').text
        authors = driver.find_element(By.XPATH, '//*[@id="ui-ncbiinpagenav-1"]/div[1]/div[2]').text
        doi = driver.find_element(By.XPATH, '//*[@id="ui-ncbiinpagenav-1"]/div[1]/div[1]/div[1]/div/div[2]/span[2]/a').text
        context = driver.find_element(By.XPATH, '//*[@id="abstract-a.adk.b.ad"]/div[2]').text
        fp = False

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/aside/div/section[2]/ul/li[1]/button')))

        # Press citation button
        driver.find_element(By.XPATH, '/html/body/main/aside/div/section[2]/ul/li[1]/button').click()
        time.sleep(2)

        reference = driver.find_element(By.XPATH, '//*[@id="ui-ncbiexternallink-3"]/div[4]/div/div[2]/div[1]').text
        result = [title, context, doi, reference, fp, authors]

        print(result)
        create_csv("text", result)


def soup_pubmed_scrapper(term):
    url = f"https://ncbi.nlm.nih.gov/pmc/?term={term}"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    # result = [title, context, doi, reference, fp, authors]

    # Get all links that are on the site that are not copies or pdfs
    result = soup.findAll('a',  href=True)
    links = []
    for element in result:
        if element['href'].__contains__('/articles')\
                and not element['href'].__contains__('pdf') and not element['href'].__contains__('/classic'):
            l_paper = {'title': element.text, 'link': nih + element['href']}
            links.append(l_paper)
    print(links)

    temp = []
    print('='*30)
    print("Get data from site")
    print('=' * 30)

    for i in links:
        if i['link'].__contains__('pdf') or i['link'].__contains__('classic'):
            continue

        title = i['title']
        page = requests.get(i['link'], headers={'User-Agent':'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, 'html.parser')
        abstract = soup.find(attrs={'id':re.compile("abstract")})
        if not abstract:
            abstract = soup.find(attrs={'id':re.compile("abs")})

        if abstract:
            abstract = abstract.text

        content = soup.contents
        text = soup.text.replace("\n", "")

    # Useful for getting sections
        # text = soup.findAll('div', id=re.compile("sec-"))
        # extract = ''
        # for element in text:
        #     extract += element.text
        # print(text)

        print(i['link'])
        list_temp = [title, i['link'], abstract, content, text]
        # print(list_temp)
        temp.append(list_temp)

    create_csv(term, temp)


def create_csv(term, data):
    csv_file = f'research_{term}'
    with open(f'data/{csv_file}.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        header = ['Title', 'Link', 'Abstract', 'XML', 'Text']
        writer.writerow(header)
        for i in data:
            writer.writerow(i)
        print(f'Successfully created file')


# def create_csv(data):
#     with open('data/research_test.csv', 'w', newline='', encoding="utf-8") as file:
#         writer = csv.writer(file)
#         header = ['Title', 'Context', 'doi', 'reference', 'Full Paper', 'Authors']
#         writer.writerow(header)
#         writer.writerow(data)


if __name__ == "__main__":
    # link = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9305720/"
    # link = f"https://ncbi.nlm.nih.gov/pmc/?term={term}"
    print('=' * 40)
    print(' ' * 11, "Starting scraper")
    print('=' * 40)
    for i in term:
        soup_pubmed_scrapper(i)
    print('=' * 40)
    print(' ' * 10, "Finished Execution")
    print('=' * 40)
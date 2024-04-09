import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests

nih = 'https://www.ncbi.nlm.nih.gov'

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
        create_csv(result)


def soup_pubmed_scrapper(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    # result = [title, context, doi, reference, fp, authors]
    result = soup.findAll('a',  href=True)
    links = []
    for element in result:
        if element['href'].__contains__('/articles'):
            l_paper = {'title': element.text, 'link': nih + element['href']}
            links.append(l_paper)
    print(links)


    print('='*30)
    print("Test\n")
    for i in links:
        page = requests.get(i['link'], headers={'User-Agent':'Mozilla/5.0'})
        print(page.text)
        break
    # create_csv(result)




def create_csv(data):
    with open('data/research_test.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        header = ['Title', 'Context', 'doi', 'reference', 'Full Paper', 'Authors']
        writer.writerow(header)
        writer.writerow(data)


if __name__ == "__main__":
    # link = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9305720/"
    link = "https://ncbi.nlm.nih.gov/pmc/?term=covid"
    print('=' * 40)
    print(' ' * 11, "Starting scraper")
    print('=' * 40)
    soup_pubmed_scrapper(link)
    print('=' * 40)
    print(' ' * 10, "Finished Execution")
    print('=' * 40)
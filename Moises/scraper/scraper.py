import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

nih = 'https://www.ncbi.nlm.nih.gov'
term = ['covid vaccine', 'covid treatment', 'covid symptoms', 'covid sickness']


def pubmed_paper_scraper(term):
    url = f"https://ncbi.nlm.nih.gov/pmc/?term={term}"
    log_count = 0
    links = []
    with webdriver.Chrome() as driver:

        driver.get(url)

        # 100-page view
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ps100"]')))
        driver.find_element(By.XPATH,
                                '//*[@id="EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.Display"]').click()
        time.sleep(5)
        button = driver.find_element(By.XPATH, '//*[@id="ps100"]')
        button.click()

        time.sleep(5)

        # Iterate to n amount of pages
        for i in range(30):
            try:
                count = 0
                # Wait for page to reload
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]')))
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                                '//*[@class="active page_link next"]')))
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Get all links that are on the site that are not copies or pdfs
                result = soup.findAll('a', href=True)

                for element in result:

                    # Prevent unverified papers from being added
                    if count == 100:
                        break

                    if element['href'].__contains__('/articles') \
                            and not element['href'].__contains__('pdf') and not element['href'].__contains__('classic') \
                            and element.text != '\n\n' and not element['href'].__contains__("?report=abstract"):

                        l_paper = {'id': log_count, 'title': element.text, 'link': nih + element['href']}
                        links.append(l_paper)
                        count += 1
                        log_count += 1

                        if log_count % 50 == 0:
                            log(f'Paper #{log_count} data: {l_paper}')

                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@class="active page_link next"]').click()
                time.sleep(1)

            except:
                log(f'Failed on paper #{log_count}')
                break

        # Print progress
        log("Data scraped successfully")

    create_csv(term, links, log_count)


def create_csv(term, data, records):
    csv_file = f'research_{term}_{records}_records'
    with open(f'data/{csv_file}.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        header = ['Id', 'Title', 'Link']
        writer.writerow(header)
        for element in data:
            temp = [element['id'], element['title'], element['link']]
            writer.writerow(temp)
        log(f'Successfully created file: {csv_file}')


def log(text):
    print(f'{round(time.time() - start_time, 2)}s: {text}')
    print('=' * 100, '\n')


if __name__ == "__main__":
    start_time = time.time()
    log("Starting Scraper")
    for i in term:
        pubmed_paper_scraper(i)

    log("Finished Execution!")

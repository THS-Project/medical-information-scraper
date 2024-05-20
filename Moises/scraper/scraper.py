import os
import csv
import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import requests
from bs4 import BeautifulSoup

nih = 'https://www.ncbi.nlm.nih.gov'
terms = ['covid vaccine', 'covid treatment', 'covid symptoms', 'covid sickness']


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

    return log_count


def soup_pubmed_scrapper(term, links):
    # Code not needed anymore
    # url = f"https://ncbi.nlm.nih.gov/pmc/?term={term}"
    # page = requests.get(url)
    #
    # soup = BeautifulSoup(page.content, 'html.parser')
    #
    # # Get all links that are on the site that are not copies or pdfs
    # result = soup.findAll('a',  href=True)
    # links = []
    # for element in result:
    #     if '/articles' in element['href'] and 'pdf' not in element['href'] and 'classic' not in element['href']:
    #         l_paper = {'title': element.text, 'link': nih + element['href']}
    #         links.append(l_paper)
    # #print(links)
    #
    # print('='*30)
    # print("Get data from site")
    # print('=' * 30)
    #
    # # testing in only one link
    # links = [{'title': 'Erythema Migrans-like COVID Vaccine Arm: A Literature Review', 'link': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8836892/'}]

    temp = []
    paper_number = 0

    for i in links:
        if 'pdf' in i['link'] or 'classic' in i['link']:
            continue

        title = i['title']
        page = requests.get(i['link'], headers={'User-Agent':'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, 'html.parser')
        abstract = soup.find(attrs={'id':re.compile("abstract")})
        if not abstract:
            abstract = soup.find(attrs={'id':re.compile("abs")})

        if abstract:
            abstract = abstract.text




        #context
        contexts = soup.find_all(class_="jig-ncbiinpagenav")

        if not contexts:
            contexts = soup.find_all(class_='article-details')
        context_text = [context.get_text() for context in contexts]

        clean_context_text = []
        for text in context_text:
            text = text.replace('\xa0', ' ')
            text = text.replace('\n', ' ')
            text = text.replace(':', ': ')
            text = ' '.join(text.split())
            clean_context_text.append(text)




        #doi number
        dois = soup.find_all(class_="doi")
        doi_number = [doi.get_text().replace('doi:\xa0', '') for doi in dois]

        if not doi_number:
            dois = soup.find_all(class_="identifier doi")
            doi_number = [doi.find('a').get_text().strip() for doi in dois]

        doi_number = list(set(doi_number))




        #references
        references = soup.find_all(class_="ref-cit-blk half_rhythm")
        if not references:
            references = soup.find_all(class_="references-and-notes-list")
        if not references:
            references = soup.find_all(class_="element-citation")

        reference_text = [reference.get_text() for reference in references]
        clean_references = []
        for ref in reference_text:
            ref = ref.strip()
            ref = ref.replace('\n', ' ')
            ref = re.sub(r'^\d+\.\s', '', ref)
            ref = ' '.join(ref.split())
            clean_references.append(ref)





        #fullpaper
        isFullpaper = soup.find_all(class_="tsec sec")
        isFullpaper2_verification = soup.find_all(class_="full-text-links-list")





        #keywords
        keywords = soup.find_all(class_="kwd-text")
        keywords_text = [keyword.get_text() for keyword in keywords]
        keywords_list = [keyword.strip() for text in keywords_text for keyword in text.split(',')]

        if not keywords_list:
            keywords_parent = soup.find_all('p')
            for parent in keywords_parent:
                if 'Keywords:' in parent.text:
                    keywords_text = parent.text.split(':')[1]
                    if ';' in keywords_text:
                        keywords_text = keywords_text.split(';')
                    elif ',' in keywords_text:
                        keywords_text = keywords_text.split(',')
                    else:
                        keywords_text = [keywords_text]

                    for keyword in keywords_text:
                        keyword = keyword.strip()
                        if keyword == keywords_text[-1]:
                            keyword = keyword.rstrip('.')
                        keywords_list.append(keyword)





        #authors
        authors = soup.find_all(class_="contrib-group fm-author")
        if not authors:
            authors = soup.find_all(class_="authors-list")

        authors_text = [author.get_text() for author in authors]
        clean_authors = []
        for author in authors_text:
            author = author.strip()
            author = ''.join([i for i in author if not i.isdigit()])
            author = ' '.join(author.split())
            for name in author.split(','):
                name = name.strip()
                # Remove unwanted characters and words
                name = re.sub(r'^[a-z†*]*\s*', '', name)
                if name in ["MD", "BA", "BS", "PharmD", "MBA", "PhD", "DDS", "MS", "MSc", "MA", "MPH", "MSN", "DNP",
                            "DO", "DVM", "EdD", "PsyD", "DrPH", "ScD", "PharmB", "BSN", "RN", "∗∗", "∗"]:
                    continue
                # Remove "and" from the start of the name
                if name.startswith('and '):
                    name = name[4:]
                if name:
                    clean_authors.append(name)





        content = soup.contents
        text = soup.text.replace("\n", "")

        #print("Link", i['link'])
        list_temp = [title, i['link'], abstract, content, text, authors_text]
        temp.append(list_temp)

        doi_string = ""
        if doi_number[0]:
            doi_string = doi_number[0]

        paper = {
            "title": title,
            "context": clean_context_text,
            "doi": doi_string,
            "references": clean_references,
            "isFullpaper": len(isFullpaper) > 1 and len(isFullpaper2_verification) == 0 and len(clean_references) > 0,
            "keywords": keywords_list,
            "authors": clean_authors,
            "term": term
        }

        directory = '../json_management/scraped_json/'
        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, f'paper_{term}_{paper_number}.json')

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(paper, f, ensure_ascii=False)

        if paper_number % 50 == 0:
            log(f'Paper #{paper_number} with term {term} was jsonify successfully')

        paper_number += 1


# CSV for links' backup
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


# Extract title and link
def read_csv(term, records):
    output = []
    csv_file = f'research_{term}_{records}_records'
    with open(f'data/{csv_file}.csv', 'r', newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(file)
        for element in reader:
            # temp = {'id': element[0], 'title': element[1], 'link': element[2]}
            temp = {'title': element[0], 'link': element[1]}
            output.append(temp)
        log(f'Successfully read file: {csv_file}')
        file.close()

    return output


# Print time and message
def log(text):
    print(f'{round(time.time() - start_time, 2)}s: {text}')
    print('=' * 100, '\n')


if __name__ == "__main__":
    start_time = time.time()
    log("Starting Scraper")
    term_list = []
    # Search for links (selenium scraper)
    # for i in term:
    #     count = pubmed_paper_scraper(i)
    #     count_list = [i, count]
    #     term_list.append(count_list)

    # Testing one file
    term_list.append(['covid vaccine', 20])

    for element in term_list:
        links = read_csv(element[0], element[1])
        soup_pubmed_scrapper(element[0], links)

    log("Finished Execution!")
import os
import csv
import time
import json
from Moises.create_log import log

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import requests
from bs4 import BeautifulSoup

nih = 'https://www.ncbi.nlm.nih.gov'
terms = ['covid vaccine', 'covid treatment', 'covid symptoms', 'covid sickness', 'swine flu',
         'bird flu', 'influenza', 'flu vaccine', 'zika', 'common cold', 'cancer', 'headache',
         'allergy', 'conjunctivitis', 'stomach aches', 'chickenpox', 'monkeypox']
link_list = []


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

        pages = 50
        # Iterate to n amount of pages
        for i in range(pages):
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

                        l_paper = {'id': count, 'title': element.text, 'link': nih + element['href']}
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
    temp = []
    paper_number = 0

    for i in links:
        try:
            if paper_number >= 400:
                break
            if 'pdf' in i['link'] or 'classic' in i['link']:
                continue

            title = i['title']
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }
            proxy = {
                'https': 'https://154.236.177.100:1977'
            }
            page = requests.get(i['link'], headers=headers, proxies=proxy)
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

                # Find all matches of the pattern in the text
                matches = list(re.finditer(r"\b(?:References|REFERENCES)+\w*", text))

                if matches:
                    last_match = matches[-1]
                    text = text[:last_match.start()].strip()  # Slice and remove everything after the Reference
                else:
                    log(f"No reference in paper {paper_number}")

                text = text.replace('\xa0', ' ')
                text = text.replace('\n', ' ')
                text = text.replace(':', ': ')
                text = ' '.join(text.split())

                clean_context_text.append(text)

            #cite
            doi = soup.find(class_='citation-button citation-dialog-trigger ctxp')
            ref_url = doi.attrs['data-all-citations-url']
            paper_ref = requests.get(f'https://ncbi.nlm.nih.gov{ref_url}')
            paper_dict = json.loads(paper_ref.text)
            doi = paper_dict['nlm']['orig']

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

            list_temp = [title, i['link'], abstract, content, text, authors_text]
            temp.append(list_temp)

            # doi_string = ""
            # if doi_number[0]:
            #     doi_string = doi_number[0]

            paper = {
                "title": title,
                "context": clean_context_text,
                "doi": doi,
                "references": clean_references,
                "isFullpaper": len(isFullpaper) > 1 and len(isFullpaper2_verification) == 0 and len(clean_references) > 0,
                "keywords": keywords_list,
                "authors": clean_authors,
                "term": term
            }

            directory = 'json_management/scraped_json/'
            os.makedirs(directory, exist_ok=True)

            file_path = os.path.join(directory, f'paper_{term}_{paper_number}.json')

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(paper, f, ensure_ascii=False)

            if paper_number % 50 == 0:
                log(f'Paper #{paper_number} with term {term} was jsonify successfully')

        except Exception as E:
            log(f'Paper #{paper_number} failed: {E}')

        finally:
            paper_number += 1


# CSV for links' backup
def create_csv(term, data, records = 0):
    csv_file = f'research_{term}_{records}_records'
    index= 0
    with open(f'data/{csv_file}.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        header = ['Id', 'Title', 'Link']
        writer.writerow(header)
        for element in data:
            temp = [index, element['title'], element['link']]
            writer.writerow(temp)
            index += 1
        log(f'Successfully created file: {csv_file}')


# Extract title and link
def read_csv(csv_file):
    output = []
    # csv_file = f'research_{term}_{records}_records'
    with open(f'scraper/data/{csv_file}', 'r', newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(file)
        for element in reader:
            temp = {'id': element[0], 'title': element[1], 'link': element[2]}
            # temp = {'title': element[0], 'link': element[1]}
            output.append(temp)
        log(f'Successfully read file: {csv_file}')
        file.close()

    return output


# Not in use
def remove_duplicates(links):
    temp_list = []
    for element in links:
        if len(link_list) < 1:
            temp_list = links
            link_list.extend(temp_list)
            return temp_list, len(temp_list)

        if element not in link_list:
            temp_list.append(element)

    link_list.extend(temp_list)
    new_length = len(temp_list)
    print(link_list)
    log(f'Removed {len(links)-new_length} duplicates')
    return temp_list, new_length


def link_scraper():
    log("Starting Scraper")
    # Search for links (selenium scraper)
    for i in terms:
        count = pubmed_paper_scraper(i)
        log(f'Scraped {count} records')


def start_scraper():
    log("Starting data cleaning")

    directory = 'scraper/data/'
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            if filename.__contains__('covid symptoms') or filename.__contains__('flu vaccine'):
                continue
            links = read_csv(filename)
            term = filename.split('_')
            soup_pubmed_scrapper(term[1], links)

    log("Finished cleaning the data")


if __name__ == "__main__":
    link_scraper()


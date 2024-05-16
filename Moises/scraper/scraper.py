import csv
import time
import re
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import re
from bs4 import BeautifulSoup

nih = 'https://www.ncbi.nlm.nih.gov'
term = ['covid vaccine', 'covid treatment', 'covid symptoms', 'covid sickness']


#Creo que no se está usando
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

# Moises scrapper
# def soup_pubmed_scrapper(term):
#     url = f"https://ncbi.nlm.nih.gov/pmc/?term={term}"
#     page = requests.get(url)
#
#     soup = BeautifulSoup(page.content, 'html.parser')
#
#     # result = [title, context, doi, reference, fp, authors]
#
#     # Get all links that are on the site that are not copies or pdfs
#     result = soup.findAll('a',  href=True)
#     links = []
#     for element in result:
#         if element['href'].__contains__('/articles')\
#                 and not element['href'].__contains__('pdf') and not element['href'].__contains__('/classic'):
#             l_paper = {'title': element.text, 'link': nih + element['href']}
#             links.append(l_paper)
#     print(links)
#
#     temp = []
#     print('='*30)
#     print("Get data from site")
#     print('=' * 30)
#
#     for i in links:
#         if i['link'].__contains__('pdf') or i['link'].__contains__('classic'):
#             continue
#
#         title = i['title']
#         page = requests.get(i['link'], headers={'User-Agent':'Mozilla/5.0'})
#         soup = BeautifulSoup(page.content, 'html.parser')
#         abstract = soup.find(attrs={'id':re.compile("abstract")})
#         if not abstract:
#             abstract = soup.find(attrs={'id':re.compile("abs")})
#
#         if abstract:
#             abstract = abstract.text
#
#         content = soup.contents
#         text = soup.text.replace("\n", "")
#
#     # Useful for getting sections
#         # text = soup.findAll('div', id=re.compile("sec-"))
#         # extract = ''
#         # for element in text:
#         #     extract += element.text
#         # print(text)
#
#         print(i['link'])
#         list_temp = [title, i['link'], abstract, content, text]
#         # print(list_temp)
#         temp.append(list_temp)

    # create_csv(term, temp)

def soup_pubmed_scrapper(term):
    url = f"https://ncbi.nlm.nih.gov/pmc/?term={term}"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all links that are on the site that are not copies or pdfs
    result = soup.findAll('a',  href=True)
    links = []
    for element in result:
        if '/articles' in element['href'] and 'pdf' not in element['href'] and 'classic' not in element['href']:
            l_paper = {'title': element.text, 'link': nih + element['href']}
            links.append(l_paper)
    #print(links)

    temp = []
    print('='*30)
    print("Get data from site")
    print('=' * 30)

    paper_number = 0
    #testing in only one link
    #links = [{'title': 'Erythema Migrans-like COVID Vaccine Arm: A Literature Review', 'link': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8836892/'}, {'title': 'Severe Acute Respiratory Syndrome Coronavirus 2: The Role of the Main Components of the Innate Immune System', 'link': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8442517/'}]
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


        paper = {
            "title": title,
            "context": clean_context_text,
            "doi": doi_number,
            "references": clean_references,
            "isFullpaper": len(isFullpaper) > 1 and len(isFullpaper2_verification) == 0 and len(clean_references) > 0,
            "keywords": keywords_list,
            "authors": clean_authors,
            "term": term
        }

        with open(f'paper_{term}_{paper_number}.json', 'w', encoding='utf-8') as f:
            json.dump(paper, f, ensure_ascii=False)

        paper_number += 1

#creo que no se está usando
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
    # for i in term:
    #     soup_pubmed_scrapper(i)
    soup_pubmed_scrapper("covid vaccine")
    print('=' * 40)
    print(' ' * 10, "Finished Execution")
    print('=' * 40)
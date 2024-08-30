import csv
import json
import os
import requests
from Moises.create_log import log


def get_pcmid(link: str) -> str:
    link_list = link.split('/')
    filter_list = list(filter(None, link_list))
    pcmid = filter_list[-1]
    return pcmid


def read_csv(csv_file: str) -> list[str]:
    output = []
    with open(csv_file, 'r', newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(file)
        for element in reader:
            pcmid = get_pcmid(element[2])
            output.append(pcmid)
        log(f'Successfully read file: {csv_file}')
        file.close()

    return output


def get_authors(authors:dict, fullName: bool = False) -> str:
    author_cite = ''
    author_list = [v for k, v in authors.items() if k.startswith('name')]

    if len(author_list) < 1:
        return author_cite

    for author in author_list:
        name = author.split(';')
        surname = name[0].split(':')[1]
        if len(name) <= 1:
            givenname = ''
        else:
            givenname = name[1].split(':')[1] if fullName else name[1].split(':')[1][0]

        author_cite += f'{surname} {givenname}, ' if givenname != '' else f'{surname}, '

    author_cite = f"{author_cite[:-2]}." if not fullName else list(filter(None, author_cite.split(', ')))

    return author_cite


def get_references(full_reference: dict) -> str:
    reference = full_reference['infons']
    # authors = [v for k, v in reference.items() if k.startswith('name')]

    # Get authors
    author_cite = get_authors(reference)

    research_name = f"{full_reference['text']}."
    source = f"{reference['source']}." if 'source' in reference else ''
    year = f"{reference['year']};" if 'year' in reference else ''
    volume = f"{reference['volume']}:" if 'volume' in reference else ''
    firstpage = f"{reference['fpage']}-" if 'fpage' in reference else ''
    lpage = f"{reference['lpage']}." if 'lpage' in reference else ''
    if 'pub-id_doi' in reference:
        doi = f"doi: {reference['pub-id_doi']}."
    elif 'article-id_doi' in reference:
        doi = f"doi: {reference['article-id_doi']}."
    else:
        doi = ''

    out_reference = f'{author_cite} {research_name} {source} {year}{volume}{firstpage}{lpage} {doi}'

    return out_reference.strip()


def get_paper_info(paper_info: list[dict]) -> dict:
    save_elements = ['abstract', 'paragraph', 'front', 'ref']
    output_dict = {}
    for paper_dict in paper_info[0]['passages']:
        paper_type = paper_dict['infons']['section_type']
        section_type = paper_dict['infons']['type']
        text = paper_dict['text']

        # If not text, remove it
        if section_type not in save_elements:
            continue

        if section_type == 'ref':
            text = get_references(paper_dict)

        # Add context
        if paper_type in output_dict:
            output_dict[paper_type] = f"{output_dict[paper_type]}\n{text}"
        else:
            output_dict[paper_type] = text

        # Add keywords
        if section_type == 'front':
            keywords_str = paper_dict['infons']['kwd']
            keywords = keywords_str.split(" ")
            output_dict['KEYWORDS'] = list(dict.fromkeys(keywords))
            output_dict['PAPER_REF'] = get_references(paper_dict)
            output_dict['AUTHORS'] = get_authors(paper_dict['infons'], True)

    return output_dict


def jsonify_paper(paper_dict: dict, paper_number: int, term: str) -> bool:
    fullPaperVal = ['ABSTRACT', 'INTRO', 'METHODS', 'DISCUSS', 'CONCL', 'REF']
    clean_context_text = ''
    for k, v in paper_dict.items():
        if k in fullPaperVal and k != 'REF':
            clean_context_text += f'{v}\n'

    paper = {
        "title": paper_dict['TITLE'],
        "context": clean_context_text,
        "doi": paper_dict['PAPER_REF'],
        "references": paper_dict['REF'].split('\n'),
        "isFullpaper": all(elements in paper_dict.keys() for elements in fullPaperVal),
        "keywords": paper_dict['KEYWORDS'],
        "authors": paper_dict['AUTHORS'],
        "term": term
    }
    directory = 'json_management/scraped_json/'
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, f'paper_{term}_{paper_number}.json')

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(paper, f, ensure_ascii=False)
            return True
    except:
        return False


def requests_papers(papers_list: list[str], term: str) -> list[dict]:
    paper_count = 1
    result = []
    for paper_id in papers_list:
        try:
            api_url = f'https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{paper_id}/unicode'
            data = requests.get(api_url).json()
            paper_info = data[0]['documents']
            output_dict = get_paper_info(paper_info)
            paperJson = jsonify_paper(output_dict, paper_count, term)
            if paperJson:
                log(f'Successfully jsonify paper #{paper_count}')

        except Exception as E:
            log(f'Failed paper #{paper_count}: {E}')

        finally:
            paper_count += 1

    return result


def start_scraper():
    log("Starting data cleaning")

    directory = 'scraper/data/'
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = f'{directory}{filename}'
            papers_ids = read_csv(file_path)
            term = filename.split('_')
            output = requests_papers(papers_ids, term[1])

    log("Finished cleaning the data")


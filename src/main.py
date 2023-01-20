import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    DOWNLOADS_DIR,
    MAIN_DOC_URL,
    MAIN_PEP_URL,
    EXPECTED_STATUS,
    CONNECTION_ERROR_MESSAGE,
    VERSION_ERROR_MESSAGE,
    DOWNLOAD_COMPLITE,
    UNEXPECTED_PEP_STATUS,
    COMMANDS_ARGUMENTS,
    PARSER_START_MESSAGE,
    PARSER_FINISH_MESSAGE,
    PROGRAM_ERROR_MESSAGE
)
from outputs import control_output
from utils import get_response, find_tag


def get_soup(response):
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    return soup


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    soup = get_soup(response)
    main_div = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1')
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    logs = []
    for section in tqdm(main_div):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        try:
            soup = get_soup(response)
            h1 = find_tag(soup, 'h1')
            dl = soup.find('dl')
            dl_text = dl.text.replace('\n', ' ')
            results.append((version_link, h1.text, dl_text))
        except ConnectionError:
            logs.append(CONNECTION_ERROR_MESSAGE.format(link=version_link))
            continue
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    soup = get_soup(response)
    sidebar = soup.find('div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise RuntimeError(VERSION_ERROR_MESSAGE)
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    soup = get_soup(response)
    main_tag = soup.find('div', {'role': 'main'})
    table_tag = main_tag.find('table', {'class': 'docutils'})
    pdf_a4_tag = table_tag.find('a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    # Если убрать BASE_DIR, pytest выдаёт ошибку
    downloads_dir = BASE_DIR / DOWNLOADS_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNLOAD_COMPLITE.format(archive_path=archive_path))


def pep(session):
    response = session.get(MAIN_PEP_URL)
    soup = get_soup(response)
    tr_tags = soup.select('#numerical-index tbody tr')
    results_count = defaultdict(int)
    logs = []
    for tr_tag in tqdm(tr_tags):
        try:
            status_pep = find_tag(tr_tag, 'td').text[1:]
            expected_status = EXPECTED_STATUS.get(status_pep, [])
            pep_link = urljoin(MAIN_PEP_URL, find_tag(tr_tag, 'a')['href'])
            response = get_response(session, pep_link)
            soup = get_soup(response)
            description = find_tag(
                soup, 'dl', attrs={'class': 'rfc2822 field-list simple'})
            td = description.find(string='Status')
            status = td.find_parent().find_next_sibling().text
            if status not in expected_status:
                logging.append(
                    UNEXPECTED_PEP_STATUS.format(
                        pep_link=pep_link,
                        status_pep=status_pep,
                        expected_status=expected_status,
                    )
                )
        except ConnectionError:
            logs.append(CONNECTION_ERROR_MESSAGE.format(link=pep_link))
    for log in logs:
        logging.info(log)
    return [
        ('Status', 'Count'),
        *results_count.items(),
        ('Total', sum(results_count.values()))
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(PARSER_START_MESSAGE)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(COMMANDS_ARGUMENTS.format(args=args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.exception(
            msg=PROGRAM_ERROR_MESSAGE.format(error=error),
            stack_info=True
        )
    logging.info(PARSER_FINISH_MESSAGE)


if __name__ == '__main__':
    main()

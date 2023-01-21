import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    DOWNLOADS_DIR,
    MAIN_DOC_URL,
    MAIN_PEP_URL,
    WHATS_NEW_URL,
    DOWNLOAD_URL,
    EXPECTED_STATUS,
    CONNECTION_ERROR_MESSAGE,
    VERSION_ERROR_MESSAGE,
    DOWNLOAD_COMPLITE,
    PATTERN,
    UNEXPECTED_PEP_STATUS,
    COMMANDS_ARGUMENTS,
    PARSER_START_MESSAGE,
    PARSER_FINISH_MESSAGE,
    PROGRAM_ERROR_MESSAGE
)
from outputs import control_output
from utils import find_tag, get_soup


def whats_new(session):
    logs = []
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(
        get_soup(
            session, WHATS_NEW_URL
            ).select(
            '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
            )
    ):
        version_link = urljoin(WHATS_NEW_URL, section.select('a')[0]['href'])
        try:
            soup = get_soup(session, version_link)
            results.append(
                (
                    version_link,
                    find_tag(soup, 'h1').text,
                    find_tag(soup, 'dl').text.replace('\n', ' '),
                )
            )
        except ConnectionError:
            logs.append(CONNECTION_ERROR_MESSAGE.format(url=version_link))
    for log in logs:
        logging.info(log)
    return results


def latest_versions(session):
    for ul in get_soup(
        session, MAIN_DOC_URL
        ).select(
            'div.sphinxsidebarwrapper ul'
    ):
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise RuntimeError(VERSION_ERROR_MESSAGE)
    results = [('Ссылка на документацию', 'Версия', 'Статус')]

    for a_tag in a_tags:
        text_match = re.search(PATTERN, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )

    return results


def download(session):
    archive_url = urljoin(
        DOWNLOAD_URL,
        get_soup(
            session, DOWNLOAD_URL
            ).select_one(
                'table.docutils td > a[href$="pdf-a4.zip"]'
            )['href']
    )
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNLOAD_COMPLITE.format(archive_path=archive_path))


def pep(session):
    results_count = defaultdict(int)
    logs = []
    for tr_tag in tqdm(
        get_soup(
            session, MAIN_PEP_URL
            ).select(
                '#numerical-index tbody tr')
    ):
        try:
            status_pep = find_tag(tr_tag, 'td').text[1:]
            expected_status = EXPECTED_STATUS.get(status_pep, [])
            pep_link = urljoin(MAIN_PEP_URL, find_tag(tr_tag, 'a')['href'])
            description = find_tag(
                get_soup(session, pep_link),
                'dl', attrs={'class': 'rfc2822 field-list simple'})
            td = description.find(string='Status')
            status = td.find_parent().find_next_sibling().text
            if status not in expected_status:
                logs.append(
                    UNEXPECTED_PEP_STATUS.format(
                        pep_link=pep_link,
                        status_pep=status_pep,
                        expected_status=expected_status,
                    )
                )
            results_count[status] += 1
        except ConnectionError:
            logs.append(CONNECTION_ERROR_MESSAGE.format(url=pep_link))
    for log in logs:
        logging.info(log)
    return [
        ('Статус', 'Количество'),
        *results_count.items(),
        ('Всего', sum(results_count.values()))
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

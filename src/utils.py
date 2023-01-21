from requests import RequestException

from bs4 import BeautifulSoup

from constants import ERROR_LOADING_PAGE, TAG_NOT_FOUND
from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        raise ConnectionError(ERROR_LOADING_PAGE.format(url=url))


def find_tag(soup, tag, attrs=None):
    search_tag = soup.find(tag, attrs=({} if attrs is None else attrs))
    if search_tag is None:
        raise ParserFindTagException(
            TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        )
    return search_tag


def get_soup(session, url, parser='lxml'):
    return BeautifulSoup(get_response(session, url).text, parser)

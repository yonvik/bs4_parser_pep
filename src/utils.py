import logging
from requests import RequestException

from constants import ERROR_LOADING_PAGE, TAG_NOT_FOUND
from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        raise ConnectionError(logging.exception(
            ERROR_LOADING_PAGE.format(url=url),
            stack_info=True
        ))


def find_tag(soup, tag, attrs=None):
    search_tag = soup.find(tag, attrs=({} if attrs is None else attrs))
    if search_tag is None:
        raise ParserFindTagException(
            TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        )
    return search_tag

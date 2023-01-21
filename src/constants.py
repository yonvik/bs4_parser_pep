from pathlib import Path
from urllib.parse import urljoin

MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent
PRETTY = 'pretty'
FILE = 'file'
RESULTS_DIR = 'results'
LOG_DIR = BASE_DIR / 'Logs'
LOG_FILE = LOG_DIR / 'parser.log'
DOWNLOADS_DIR = 'downloads'
DOWNLOAD_URL = urljoin(MAIN_DOC_URL, 'download.html')
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')

CONNECTION_ERROR_MESSAGE = 'Ошибка соединения с {link}'
DOWNLOAD_COMPLITE = 'Архив был загружен и сохранён: {archive_path}'
VERSION_ERROR_MESSAGE = 'Данная версия Python не найдена'
UNEXPECTED_PEP_STATUS = (
    '\nОшибка в совпадении статусов по адресу: {pep_link} \n'
    'Статус: {status_pep} не найден \n'
    'Ожидаемый статус: {expected_status}'
)
COMMANDS_ARGUMENTS = 'Аргументы командной строки: {args}'
PARSER_START_MESSAGE = 'Парсер запущен!'
PARSER_FINISH_MESSAGE = 'Парсер завершил работу.'
PROGRAM_ERROR_MESSAGE = 'Ошибка в ходе выполнения программы {error}'
FILE_SAVED = 'Файл с результатами был сохранен: {file_path}'
ERROR_LOADING_PAGE = 'Возникла ошибка при загрузки страницы {url}'
TAG_NOT_FOUND = 'Не найден тег {tag} {attrs}'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
PATTERN = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

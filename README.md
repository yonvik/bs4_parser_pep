# Проект парсинга PEP

### Описание
С помощью данного парсера можно:
 - cобирать ссылки на статьи о нововведениях в Python, переходить по ним и забирать информацию об авторах и редакторах статей ;
 - собирать информацию о статусах версий Python;
 - скачивать архив с актуальной документацией;
 - собирать информацию о статусах PEP и их количествах.
 
 ### Используемые технологии
  - Python 3.9
  - BeautifulSoup4
  
 ### Порядок запуска
 1. Клонировать проект.
 ```
 git@github.com:yonvik/bs4_parser_pep.git
 ```
 2. Создать и активировать виртуальное окружение. Установить зависимости.
 ```
 python -m venv venv #(for Windows)
 ```
 ```
 python3 -m venv venv #(for MacOs/ Linux)
 ```
 ```
 python -m pip install --upgrade pip
 ```
 ```
 pip install -r requirements.txt
 ```
 3. Запустить нужную функцию парсера.
 ```
 python main.py whats-new|latest-versions|download|pep 
 ```
  - ```whats-new``` — нововведения Python;
  - ```latest-versions``` — информация о последних версиях;
  - ```download``` — загрузка документации;
  - ```pep``` — парсинг информации по каждому PEP.

 Опциональные аргументы:
  - ```-c``` | ```--clear-cache``` — очистка кеша;
  - ```-o {pretty,file}``` | ```--output {pretty,file}``` — вывод данных парсинга (таблицей в терминале/файлом).

## Примеры работы парсинга:

Команда ```whats-new``` переходит на страницу ```https://docs.python.org/3/```, собирает ссылки на каждую версию ***Python***. 
Сканирует карточку каждой версии ***Python*** и выводит результат: ссылка на статью, заголовок, редактор, автор.

Пример:
```bash
python main.py -o pretty whats-new

+----------------------------------------------+---------------------------+-----------------------------------------------------------------------+
| Ссылка на статью                             | Заголовок                 | Редактор, Автор                                                       |
+----------------------------------------------+---------------------------+-----------------------------------------------------------------------+
| https://docs.python.org/3/whatsnew/3.11.html | What’s New In Python 3.11 |  Release 3.11.1  Date January  20, 2023  Editor Pablo Galindo Salgado |
| ...                                          | ...                       |  ...                                                                  |
+----------------------------------------------+---------------------------+-----------------------------------------------------------------------+
```
---

Команда ```latest-versions``` переходит на страницу ```https://docs.python.org/3/``` и выводит результат о **Python**: ссылку на документацию, версия и статус.


Пример:
```bash
python main.py -o pretty latest-versions

+--------------------------------------+--------------+----------------+
| Ссылка на документацию               | Версия       | Статус         |
+--------------------------------------+--------------+----------------+
| https://docs.python.org/3.12/        | 3.12         | in development |
| https://docs.python.org/3.11/        | 3.11         | stable         |
| https://docs.python.org/3.10/        | 3.10         | stable         |
| https://docs.python.org/3.9/         | 3.9          | security-fixes |
| https://docs.python.org/3.8/         | 3.8          | security-fixes |
| https://docs.python.org/3.7/         | 3.7          | security-fixes |
| https://docs.python.org/3.6/         | 3.6          | EOL            |
| https://docs.python.org/3.5/         | 3.5          | EOL            |
| https://docs.python.org/2.7/         | 2.7          | EOL            |
| https://www.python.org/doc/versions/ | All versions |                |
+--------------------------------------+--------------+----------------+
```
---
Команда ```download``` переходит на страницу ```https://docs.python.org/3/download.html``` и скачивает PDF-файл документации zip-архивом. Архив сохраняется в директорию */downloads*.

Пример:
```
python main.py download
```
---
Сброр статусов документов ```pep``` на странице ```https://peps.python.org/```, и подсчёт всех **PEP** статусов документов с опцией вывода результата в csv-файл:

```
Пример:
```bash
python main.py pep -o file

Содержимое файла **pep_2023-01-20_22-38-36.csv**:

|Статус     | Количество |
|-----------|------------|
|Active     | 37         |
|Withdrawn  | 55         |
|Final      | 263        |
|Superseded | 20         |
|Rejected   | 120        |
|Deferred   | 36         |
|April Fool!| 1          |
|Accepted   | 42         |
|Draft      | 28         |
|Всего      | 602        |
```
Ознакомиться с командами непосредственно во время работы с программой можно с помощью команды:
```
python main.py --help
```
 
 ## Разработчик - [Андрей Янковский](https://github.com/yonvik) ##

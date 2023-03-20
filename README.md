## Выполненное тестовое задание компании "Каналсервис"

Скрипт находится в папке "scripts" его функционал разделен на несколько модулей:

<ul>
  <li><b>rate_cbr.py</b> - Делает запрос на сайт ЦБ РФ и берёт котировки по текущей дате. Сохраняет данные в cbr.xml и возвращает курс доллара. Если дата в cbr.xml актуальна, запрос на сервер не делается.</li>
  <li><b>sheets_get_values.py</b> - Скрипт берёт данные из Google таблицы, а так же обрабатывает ошибки при заполнении. Таблица должна заполняться только целыми              числами. Для подключения к таблице credentials.json и toke.json самостоятельно обновляются.</li>
  <li><b>script.py</b> - Основной скрипт. Проверяет актуальность данных каждую секунду, можно увеличить или уменьшить период проверки изменив timeout=1. Последние актуальные данные копируются в last_data.txt. Если данные Google таблицы изменилсь то БД обновляется выводя принты в терминал.</li>
</ul>

Cсылка на копию таблицы --> https://docs.google.com/spreadsheets/d/1YQ8aSsxAe36w25PmsAgAkk21Ij6hXafh3OAYQ8xpCzw/edit#gid=0

## Установка и запуск:

Установка с помощью <code>docker-compose.yml</code>:
<pre>
$ git clone https://github.com/impuls64s/tz_CanalService.git
$ cd tz_CanalServic
$ docker-compose up
</pre>

Полная установка:  
Требуется Python 3.7 и выше и База данных PostgreSql.  
Необходимо в корне проекта создать файл <b>.env</b> и записать туда свои значения переменных для PostgreSQL. 

<pre>
POSTGRES_DB=my_database
POSTGRES_USER=root
POSTGRES_PASSWORD=hobbit
</pre>

<pre>
$ git clone https://github.com/impuls64s/tz_CanalService.git
$ cd tz_CanalService
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python3 manage.py migrate

<i>Запускаем скрипт, для остановки Ctrl + C</i>
$ python3 scripts/script.py

<i>Открываем еще один терминал и запускаем веб-приложение. Открываем http://127.0.0.1:8000/ и видим таблицу из БД</i>
$ python3 manage.py runserver

<i>Примерно такие принты будут в терминале:</i>
[INFO] Данные в Google таблице не изменились.
[INFO] Данные в Google таблице не изменились.
[+] Google таблица изменилась, обновляю БД
[+] Внесение изменений в БД: Добавлено: 0 | Обновлено: 1 | Удалено: 0 записи.
[INFO] Данные в Google таблице не изменились.
</pre>

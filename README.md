# currency

Веб сервис для просмотра курса валют.

Для реализации использовался Python/Flask. Flask - это микрофреймворк, позволяющий реализовывать веб-приложения, а так
же работать с базами данных (создание, модификация, миграция), и т.д.

## Структура
- Серверная часть:
    - currency_get.py - опрашивает ЦБ РФ, сохраняет данные о курсах валют в БД, 
    удаляет устаревште данные из БД
- Веб-приложение:
    - currency_show.py - Flask приложение. Указывается как значение переменной
    окружения FLASK_APP. Ничего особо не делает кроме import'а из currency_show.
    - currency_show - само веб приложение.
        - migrations - служебная информация для Flask-Migrate.
        - templates - каталог с html шаблонами.
        - models.py - файл с описанием структуры БД.
        - routes.py - скрипт, формирующий веб страницы. 
- Консольная утилита:
    - curr_today.py - отображает в консоли курсы валют за сегодня
- Вспомогательные компоненты для развёртывания:
    - Dockerfile - файл для формирования docker контейнера
    - boot.sh - скрипт, настраивающий БД, cron и запускающий веб сервер.

## Развертывание
Развертывание реализовано на Docker контейнерах.

## Сбор информации
В контейнере сначала настривается cron. Каждый день в 15:00(12:00 UTC) cron запускает скрипт currency_get.py. Этот
скрипт собирает информацию с сайта ЦБ РФ, сохраняет её в базу данных. Он же удаляет устаревшие записи из базы, что бы
она не разрасталась.

## Веб приложение
Для реализации веб приложения был выбран фреймворк Flask. Приложение содержит 3 страницы:
- главная страница "/" - отображает список курсов валют
- "/week" - отображает изменение для выбранной валюты за неделю. На эту страницу можно попасть, перейдя по ссылку с
    главной
- "/day" - выдаёт текст в формате json
Внутри контейнера запущен веб сервер gunicorn, который "крутит" Flask приложение, внутри контейнера оно доступно
на порту 5000.

## База данных
Для работы с БД используется модуль Flask-SQLAlchemy. Он позволяет работать с разными БД прозрачно для разработчика.
Структура БД приведена в currency_show/models.py. Таблицы описываются в виде классов.
Таблица Currencies содержит описание валют: уникальный идентификатор (первичный ключ), взятый с сайта ЦБ РФ, и русское
название.
Таблица Rates содержит информацию об изменении валют: идентификатор + дата (составной первичный ключ), значение. Такой
первичный ключ позволяет защитить таблицу от повторяющихся значений.
Тип базы данных определяется переменной окружения DATABASE_URL. Эта переменная окружения считывается в config.py, если
она не установлена, то создаётся локальная база sqlite в ./dbdata/curr.db.
Для миграции БД используется Flask-Migrate.

## Запуск c SQLite
В каталоге проекта нужно запустить построение контейнера
$ docker build -t currency_alpine:latest .
Запускать сам контейнер предлагается, перебросив порт http сервера контейнера на 8000 порт хоста (можно любой другой),
сохранив базу данных на диске, что бы не терять данные (-v /app/dbdata:/var/lib/sqlite):
$ docker run --name currency_alpine -p 8000:5000  -v /var/lib/sqlite:/app/dbdata --rm currency_alpine:latest
Доступ к приложению в браузере:
 - http://localhost:8000 - покажет веб страницы в браузере
Доступ через консольную утилиту:
$ curr_today.py
выведет курсы валют за сегодня в stdout. По умолчанию будет пытаться соединиться
с http://localhost:8000/day. Если порт другой, то нужно задать адрес первым параметром:
$ curr_today.py localhost:<port_num>

При построении контейнера делается первая запись в базу данных (что бы не было пустых страниц). Обновление курса валют
на сайте ЦБ РФ происходит с 12:00 до 14:00, поэтому по cron'у currency_get.py собирает информацию в 15:00. Если в базу
были занесены устаревшие данные (контейнер запущен до 15:00), то в 15:00 они обновятся по cron'у.



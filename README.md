![](https://img.shields.io/badge/Python-3.7.5-blue) 
![](https://img.shields.io/badge/Django-2.2.16-green)
![](https://img.shields.io/badge/DjangoRestFramework-3.12.4-red)
<br><br>
## Название проекта
**«YaMDb API»** - проект YaMDb собирает отзывы пользователей на различные произведения.

**Возможности приложения:**<br>
:black_small_square: Регистрация на сайте, получение токена, изменение данных своей учетной записи<br>
:black_small_square: Раздаление прав пользователей согласно, назначенной ему роли<br>
:black_small_square: Возможность, согласно авторизации выполнять следующие дествия: получать, добавлять и удалять - категорию, жанр, произведение, отзыв и комментарий<br>
:black_small_square: Администрирование пользователями<br><br>


## :computer: Технологии в проекте

:small_blue_diamond: Python <br>
:small_blue_diamond: Django <br>
:small_blue_diamond: Django REST Framework <br><br>


## :pencil2: Инструкции по запуску

Клонировать репозиторий, создать и активировать виртуальное окружение:

```sh
git clone https://github.com/Amaterasq/api_yamdb.git
cd api_yatube
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Наполнить БД тестовыми данными выполнив команду:

```
python manage.py dbfill
```

Запустить проект:

```
python manage.py runserver
```

<br>

## :books: Документация
Для того чтобы получить, описанные понятным языком эндпоинты и настройки, да ещё с примерами запросов, да ещё с образцами ответов!
Читай ReDoc, документация в этом формате доступна по ссылке:

```html
 http://127.0.0.1:8000/redoc/
```

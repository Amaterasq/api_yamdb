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
git clone https://github.com/master-cim/api_yamdb-master.git
cd api_yatube-master
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
Перейти в папку приложения
```
cd cpi_yamdb
```


Выполнить миграции:

```
python manage.py migrate
```

Наполнить БД тестовыми данными выполнив команду:

```
python manage.py dbfill
```
Создать суперпользователя
```
python manage.py createsuperuser
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

<br>

## :bust_in_silhouette: Авторы проекта 

### :small_orange_diamond: Влад Перепечко _(Vlad Vi. Perepechko)_
```html
e-mail: perepechcko.vlad@ya.ru
```
```html
https://github.com/Amaterasq
```

### :small_orange_diamond: Алексей Богов _(Alexey Mi. Bogov)_
```html
e-mail: bogov-alexey@yandex.ru
```
```html
https://github.com/BogovAlex
```

### :small_orange_diamond: Светлана  Петрова _(Svetlana Yu. Petrova)_
```html
e-mail: master-cim@yandex.ru
```
```html
https://github.com/master-cim
```
![Svetlana Yu. Petrova](https://scontent-iev1-1.xx.fbcdn.net/v/t1.6435-9/p206x206/101204812_2968762206526462_4647695449438814208_n.jpg?_nc_cat=102&ccb=1-5&_nc_sid=da31f3&_nc_ohc=HlW3XVYBr3MAX8bhEGi&_nc_ht=scontent-iev1-1.xx&oh=00_AT-SmL9NzrKGJR1Omw4dt7rbXW-NNr_pcrXXOTM0V5fMuQ&oe=62086683 "Svetlana Yu. Petrova")

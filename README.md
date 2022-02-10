# Название проекта 
## «YaMDb API»
api_yamdb
# Описание
## Проект YaMDb собирает отзывы пользователей на различные произведения.
Возможности приложения:
- [X] Регистрация на сайте, получение токена, изменение данных своей учетной записи.
- [X] Раздаление прав пользователей согласно, назначенной ему роли. 
- [X] Возможность, согласно авторизации выполнять следующие дествия: получать, добавлять и удалять - категорию, жанр, произведение, отзыв и комментарий.
- [X] Администрирование пользователями.


# Технологии в проекте
- [ ] Django REST Framework
- [ ] Python
# Инструкции по запуску
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Amaterasq/api_yamdb.git
```

```
cd api_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
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
# Примеры
:white_check_mark: Для того чтобы получить, описанные понятным языком эндпоинты и настройки, да ещё с примерами запросов, да ещё с образцами ответов!
Читай ReDoc, документация в этом формате доступна по ссылке:

```html
 http://127.0.0.1:8000/redoc/
```

# Авторы проекта 
### Влад Перепечко
```html
e-mail:
```
```html
https://github.com/Amaterasq
```

### Алексей Богов_
_(Alexey Mi. Bogov)_
```html
e-mail: bogov-alexey@yandex.ru
```
```html
https://github.com/BogovAlex
```

### Светлана  Петрова_
_(Svetlana Yu. Petrova)_
```html
e-mail: master-cim@yandex.ru
```
```html
https://github.com/master-cim
```
![Svetlana Yu. Petrova](https://scontent-iev1-1.xx.fbcdn.net/v/t1.6435-9/p206x206/101204812_2968762206526462_4647695449438814208_n.jpg?_nc_cat=102&ccb=1-5&_nc_sid=da31f3&_nc_ohc=HlW3XVYBr3MAX8bhEGi&_nc_ht=scontent-iev1-1.xx&oh=00_AT-SmL9NzrKGJR1Omw4dt7rbXW-NNr_pcrXXOTM0V5fMuQ&oe=62086683 "Svetlana Yu. Petrova")
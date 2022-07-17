[![CI](https://github.com/yandex-praktikum/hw05_final/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/yandex-praktikum/hw05_final/actions/workflows/python-app.yml)

## Yatube – _это социальная сеть блогеров_
___

Веб-приложение, позволяет  пользователям  создать учетную запись, публиковать записи, подписываться на любимых авторов
и отмечать понравившиеся записи.
___
### Технологии

- Python 3.8
- Django 2.2.19 
- Pytest 
- Pillow 
- Bootstrap
___
___

- Разработан по классической MVT архитектуре.
- Используется пагинация постов и кеширование.
- Регистрация реализована с верификацией данных, сменой и восстановлением пароля через почту.
___

### Запуск проекта в dev-режиме
Чтобы запустить это приложение, вам потребуeтся установленный на вашем компьютере Git.

- Клонируйте этот репозиторий на свой локальный компьютер
  
```
git clone https://github.com/sniki-ld/Yatube
```
- Установите и активируйте виртуальное окружение
  
```
python3 -m venv env
```
```
source env/bin/activate
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 

- Примените миграции:

```
python manage.py migrate
```
- Для доступа к панели администратора создайте администратора:
```
python manage.py createsuperuser
```
- В папке с файлом manage.py выполните команду:
```
python manage.py runserver
```
___
### Автор
Елена Денисова

# DjangoShopApp
A Django-based online shop web application

This project requires PostgreSQL and Python with Django, psycopg2, and Pillow installed.

Default settings:
- Database name: shop
- User: postgres
- Password: 12345678
- Host: localhost
- Port: 5432

Instructions:
- Create a new Django project with `django-admin startproject projectname`.
- `cd` to the newly created project directory.
- Create the app with `python manage.py startapp shopapp`.
- Replace files in the directory with the source code.
- Run `python manage.py makemigrations`.
- Run `python manage.py migrate`.
- Create an admin account with `python manage.py createsuperuser`.
- Run the project with `python manage.py runserver`.
- Access the web app typically via `http://127.0.0.1:8000/`.

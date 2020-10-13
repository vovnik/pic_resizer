Веб-приложение на для загрузки картинок и изменения их размера.
Написано на Python 3.8.5/Django 3.1.2

Установка:
	1. Создайте новое виртуальное окружение с помощью команды 'python3 -m venv resizer_env' и перейдите в созданную директорию.
	2. Загрузите приложения с git-репозитория командой 'git clone https://github.com/vovnik/pic_resizer'
	3. Активируйте виртуальное окружение (в UNIX-системах командой 'source bin/activate')
	4. Задайте в переменной окружения DJANGO_SECRET_KEY секретный ключ приложения (в UNIX-системах командой 'export DJANGO_SECRET_KEY=...')
	5. Активируйте скриптом init.sh/init.bat загрузку необходимых библиотек и миграцию базы данных.
	6. Приложение должно быть запущено. Остановить его работу можно сочетанием CTRL+C
	7. Запускать приложение с помощью запуска скрипта manage.py в основной папке проекта можно следующим образом: 'python manage.py runserver'
	8*. Опытный пользователь может настроить запуск приложения через Gunicorn в качестве application-сервера с помощью wsgi-воркера picresizer/wsgi.py
	9*. Вместе с Gunicorn следует настраивать nginx для проксирования запросов из сети и раздачи статических файлов(в.т.ч. картинок) 

Приложение преставляет из себя сайт со следующими страницами:
	1. '/' : заглавная страница со списком загруженных изображением и ссылкой на страницу загрузки нового изображения.
	2. '/upload/' : страница загрузки нового приложения. Форма загрузки позволяет указать URL изображения в сети или загрузить его со своего компьютера.
	3. '/picture/{id}' : страница изображения с формой для ввода ширины/высоты изображения в пикселях. По умолчанию изображение выводится в оригинальном размере. Изменять размер изображения можно с помощью отправки формы с необходимым размером страницы. Перезагрузка страницы без отправки формы возвращает изначальный размер изображения.
	
P.S. HTML-форма для загрузки картинки сделана вручную, чтобы исключить HTML-валидацию исходя из ТЗ.
     Присутствует частичное покрытие тестами.

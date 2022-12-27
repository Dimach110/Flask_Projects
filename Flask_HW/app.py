from flask import Flask
from flask_bcrypt import Bcrypt

# Создаём приложение Flask
advApp = Flask('advertisement')

# отключаем автоматическую сортировку при выводе данных json
advApp.config['JSON_SORT_KEYS'] = False

# добавляем возможность шифровать пароли
bcrypt = Bcrypt(advApp)
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt

# Создаём приложение Flask
advApp = Flask('advertisement')
bcrypt = Bcrypt(advApp)
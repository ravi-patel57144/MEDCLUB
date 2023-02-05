from flask import Flask
# from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CSRFProtect

# from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)

app.config['SECRET_KEY']='b4491168f49f7b962953f8a6a3eaa6e7'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://medclub:password123@localhost:3306/dbsite'
db=SQLAlchemy(app)


from medclub import routes
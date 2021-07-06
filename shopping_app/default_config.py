from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

DEBUG = True
DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

LOG_LOCATION = ''

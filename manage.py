from flask_script import Manager

from shopping_app import create_app
from shopping_app.database import init_db, drop_db
from flask_migrate import MigrateCommand

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    print('Initialising database')
    init_db()
    print('Database initialized')
    

@manager.command
def dropdb():
    print('Dropping database')
    drop_db()
    print('Database dropped')
    

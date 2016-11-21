from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
#documentation Flask-Migrate https://flask-migrate.readthedocs.io/en/latest/

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/dataBaseSite'

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
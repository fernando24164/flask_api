#!/usr/bin/env python
from app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from app.api.models import User, Weather_Station

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                Weather_Station=Weather_Station)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)
manager.add_command("run", Server(host='0.0.0.0',
                                  port=5000,
                                  use_debugger=False))


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def migrate():
    """Make migrations"""
    from flask_migrate import upgrade
    from app.api.models import User, Weather_Station

    upgrade()

    User.insert_users()
    Weather_Station.insert_stations()


@manager.command
def reset():
    """Reset the database"""
    from flask_migrate import downgrade

    downgrade()


if __name__ == '__main__':
    manager.run()

from app import create_app, db, guard
from app.usermanagement.models import UsermanagementModel
from flask_script import Manager
import unittest
import coverage
import os
from datetime import datetime as dt
from flask_migrate import Migrate, MigrateCommand


app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """
        Runs the unit tests without generates a coverage report on success.
        :return:
    """

    tests = unittest.TestLoader().discover('tests', pattern='*_test.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """
    Runs the unit tests and generates a coverage report on success.
    While the application is running, you can run the following command in a new terminal:
    'docker-compose run --rm flask python manage.py cov' to run all the tests in the
    'tests' directory. If all the tests pass, it will generate a coverage report.
    :return int: 0 if all tests pass, 1 if not
    """

    cov = coverage.coverage(branch=True, include='tests/*', omit='*__.py')
    cov.start()
    tests = unittest.TestLoader().discover('tests', pattern='*_test.py')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary: ')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()

@manager.command
def insert_admin():
    admin = UsermanagementModel(
        username="admin",
        password=guard.hash_password("admin"),
        roles="admin",
        created_by="admin",
        date_modified=dt.now(),
        modified_by="admin"
    )

    user = UsermanagementModel.lookup("admin")

    if not user:
        try:
            # admin.save_to_db()
            print("okes")
            return "admin inserted"
        except Exception as e:
            return e
    else:
        return "{} already exists".format(user.username)

@manager.command
def test_file(dir):
    """
    run this for test file
    :param file:
    :return:
    """
    tests = unittest.TestLoader().discover('tests/'+dir, pattern='*_test.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()

import os
import unittest

from flask_migrate import Migrate, MigrateCommand

from app import blueprint
from app.main import create_app, db
from app.main.model import user, blacklist

app = create_app(os.getenv('FLASK_ENV') or 'development')
app.register_blueprint(blueprint)

app.app_context().push()

migrate = Migrate(app, db)

@app.cli.command("test")
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    app.run()

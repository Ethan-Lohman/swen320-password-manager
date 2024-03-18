from flask.cli import FlaskGroup
from web import app
from decouple import config
import unittest

cli = FlaskGroup(app)

@cli.command("test")
def test():
    app.config.from_object(config("APP_SETTINGS", default="config.DevelopmentConfig"))

    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=10).run(tests)

    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == "__main__":
    cli()

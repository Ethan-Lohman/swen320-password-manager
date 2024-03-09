from flask.cli import FlaskGroup
from web import app
from decouple import config  # Import the config function from decouple
import unittest

cli = FlaskGroup(app)

@cli.command("test")
def test():
    """Runs the unit tests without coverage."""
    # Set the configuration here or ensure it's set in your Flask app
    app.config.from_object(config("APP_SETTINGS", default="config.DevelopmentConfig"))

    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=10).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == "__main__":
    cli()

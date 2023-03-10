import unittest
import sys
from flask import url_for

from . import commands_bp
from ..extension import FlaskApp

@commands_bp.cli.command('test')
def test():
    tests = unittest.TestLoader().discover("test", pattern='*.py')#對test資料夾下，所有.py都抓進來
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)


@commands_bp.cli.command('url_map')
def list_routes():
    app = FlaskApp().app
    with app.app_context(), app.test_request_context():
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint} {rule.methods} {rule.arguments}")

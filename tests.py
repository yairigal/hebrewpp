import sys
from contextlib import contextmanager
from io import StringIO

import pytest

from hebrewpp import run


@contextmanager
def capture_stdout():
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    yield sys.stdout
    sys.stdout = old_stdout


def test_if():
    code = f"""
אם 5 > 3:
    הדפס שלום
"""
    with capture_stdout() as stdout:
        run(code)
        assert stdout.getvalue().strip('\n') == 'שלום'

def test_print():
    code = f"""הדפס מילים מלא"""
    with capture_stdout() as stdout:
        run(code)
        assert stdout.getvalue().strip('\n') == 'מילים מלא'

def test_variable_definition():
    code = f"""
א = 5
הדפס א"""
    with capture_stdout() as stdout:
        run(code)
        assert stdout.getvalue().strip('\n') == '5'

def test_nameerror():
    code = f"""
א = 5
אם ב > 5:
    הדפס שלום"""
    with pytest.raises(NameError, match=f"ב not found"):
        run(code)
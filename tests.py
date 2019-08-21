import os

import pytest

from model import create_schema

def setup_module():
    create_schema(os.environ['DATABASE_URL'])

def test_schema():
    assert 1 == 1



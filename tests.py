import os

import pytest

from model import create_schema, get_session
from mockdata import create_mock_data 

DB_URL = os.environ['DATABASE_URL'])

def setup_module():
    create_schema(db_url)
    create_mock_data(db_url)

def test_schema():
    assert 1 == 1



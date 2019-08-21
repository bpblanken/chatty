import os

import pytest

from model import create_schema, get_session
from mockdata import create_mock_data 

DB_URL = os.environ['DATABASE_URL']

def setup_module():
    create_schema(DB_URL)
    create_mock_data(DB_URL)

def test_schema():
    session = get_session()
    users = session.query(model.User).all()
    assert len(users) == 2



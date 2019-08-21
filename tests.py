import os

import pytest

from model import create_schema
from mockdata import create_mock_data 

def setup_module():
    create_schema(os.environ['DATABASE_URL'])
    create_mock_data(os.environ['DATABASE_URL'])

def test_schema():
    assert 1 == 1



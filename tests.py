import os

import pytest

from model import * 
from mockdata import create_mock_data 

from chatty import DB_URL

def setup_module():
    create_schema(DB_URL)
    create_mock_data(DB_URL)

def test_schema():
    session = get_session(DB_URL)
    users = session.query(User).all()
    assert len(users) == 2
    
    my_user = session.query(User) \
                .filter(User.name == 'Ben') \
                .one()
    assert my_user.gender == Gender.MALE
    assert my_user.age == 27
    assert len(my_user.send_events) == 2

    receive_event1 = my_user.receive_events[0]
    assert receive_event1.question.topic.title == "TEMPERATURE"
    assert receive_event1.text == "97 degrees"





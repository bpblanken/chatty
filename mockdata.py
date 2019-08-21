from model import *

def create_mock_data(conn_string):
    session = get_session(conn_string)

    topic1 = Topic("TEMPERATURE")
    topic2 = Topic("SYMPTOMS")

    question1 = Question("What is your temperature?")
    question1.topic = topic1
    question2 = Question("Do you have a cough?")
    question2.topic = topic2
    question3 = Question("Do you have a fever?")
    question3.topic = topic3


    session.add_all(
        [
            topic1,
            topic2,
            question1,
            question2,
            question3
        ]
    )

    session.commit()

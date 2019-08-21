import os

import inquirer

from model import *
from mockdata import create_mock_data

DB_URL = os.environ['DATABASE_URL']

def list_question_texts(session, topic_title):
    pass


def prompt_question_topic(session):
    questions = [
        inquirer.List('question_topic',
            message='Which question topic would you like to interact with?',
            choices=session.query(Topic.title).all()
        )
    ]
    answers = inquirer.prompt(questions)
    return answers[0] if answers else None

def main():
    session = get_session(DB_URL)
    create_mock_data(session)
    with session:
        topic = prompt_question_topic(session)
        print(topic)

if __name__ == '__main__':
    main()

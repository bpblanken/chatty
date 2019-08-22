import os

import inquirer

from model import *
from mockdata import create_mock_data

DB_URL = os.environ['DATABASE_URL']

def list_question_texts(session, topic_title):
    pass

def list_questions_for_selected_topic(session, topic_title):
    return session.query(Question) \
                  .filter(Question.topic.title == topic_title) \
                  .all()

def prompt_question_topic(session):
    tty_questions = [
        inquirer.List('question_topic',
            message='Which question topic would you like to interact with?',
            choices=[str(x[0]) for x in session.query(Topic.title).all()]
        )
    ]
    answers = inquirer.prompt(tty_questions)
    return answers['question_topic'] if answers else None

def main():
    create_schema(DB_URL)
    create_mock_data(DB_URL)
    session = get_session(DB_URL) 
    topic_title = prompt_question_topic(session)
    questions = list_questions_for_selected_topic(session, topic_title)
    for question in questions:
        print(question)

if __name__ == '__main__':
    main()

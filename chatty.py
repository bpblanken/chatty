import os

import inquirer

from model import *

DB_URL = os.environ['DATABASE_URL']

def prompt_question_topic(session):
    questions = [
        inquirer.List('question_topic',
            message='Which question topic would you like to interact with?'
            choices=[session.query(Topic.title).all()]
    ]
    answers = inquirer.prompt(questions)
    return answers[0] if answers else None

def main():
    session = get_session(DB_URL)
    with session:
        topic = prompt_question_topic(session)
        print(topic)

if __name__ == '__main__':
    main()

import os

import inquirer

from model import *
from mockdata import create_mock_data

DB_URL = os.environ['DATABASE_URL']

def list_questions_for_selected_topic(session, topic_title):
    return session.query(Question) \
                  .join(Question.topic) \
                  .filter(Topic.title == topic_title) \
                  .all()

def insert_new_text(session, question_id, new_text):
    question_text = QuestionText(new_text)
    question_text.question_id = question_id
    session.add(question_text)
    session.commit()

def prompt_question_topic(session):
    tty_questions = [
        inquirer.List('question_topic',
            message='Which question topic would you like to interact with?',
            choices=[str(x[0]) for x in session.query(Topic.title).all()]
        )
    ]
    answers = inquirer.prompt(tty_questions)
    return answers['question_topic']

def prompt_question_modify_text(session, questions):
    tty_questions = [
        inquirer.List('question_id',
            message="Would you like to edit the text for a question?",
            choices=[str(question.id) for question in questions]
        )
    ]
    answers = inquirer.prompt(tty_questions)
    return answers['question_id'] 

def prompt_for_new_text(session, question_id):
    tty_questions = [
        inquirer.Text('new_text',
            message=f"What's the new question text for Question #{question_id}?"
        ),
    ]
    answers = inquirer.prompt(tty_questions)
    return answers['new_text']

def display_questions(questions):
    print("Here's the questions for that topic!")
    for question in questions:
        print(question)

def main():
    create_schema(DB_URL)
    create_mock_data(DB_URL)
    session = get_session(DB_URL) 
    topic_title = prompt_question_topic(session)
    questions = list_questions_for_selected_topic(session, topic_title)
    display_questions(questions)
    question_id = prompt_question_modify_text(session, questions) 
    new_text = prompt_for_new_text(session, question_id)
    insert_new_text(session, question_id, new_text)
    
    print("Querying to verify...")
    questions = list_questions_for_selected_topic(session, topic_title)
    display_questions(questions)
    
if __name__ == '__main__':
    main()

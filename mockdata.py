from model import *

def create_mock_data(conn_string):
    session = get_session(conn_string)

    topic1 = Topic("TEMPERATURE")
    topic2 = Topic("SYMPTOMS")

    question1 = Question()
    question1.topic = topic1
    question1.question_texts = [QuestionText("What is your temperature")]
    question2 = Question()
    question2.topic = topic2
    question2.question_texts = [
        QuestionText("Do you have a runny nose"), 
        QuestionText("Is your nose runny?")
    ]   
    question3 = Question()
    question3.topic = topic2
    question3.question_texts = []

    user1 = User('Ben', Gender.MALE, 27)
    user2 = User('Jim', Gender.NON_BINARY, 23)

    send_event1 = SendEvent()
    send_event1.user = user1
    send_event1.question = question1

    send_event2 = SendEvent()
    send_event2.user = user1
    send_event2.question = question2

    send_event3 = SendEvent()
    send_event3.user = user2
    send_event3.question = question2

    receive_event1 = ReceiveEvent("97 degrees")
    receive_event1.user = user1
    receive_event1.question = question1
    
    session.add_all(
        [
            topic1,
            topic2,
            question1,
            question2,
            question3,
            user1,
            user2,
            send_event1,
            send_event2,
            send_event3,
            receive_event1
        ]
    )

    session.commit()

import csv
import os
QUESTIONS = "C:/Users/salon/Codecool/ask-mate-1-python-AdrianRymaszewski/sample_data/question.csv"
ANSWERS = "C:/Users/salon/Codecool/ask-mate-1-python-AdrianRymaszewski/sample_data/answer.csv"
QUESTIONS_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message"]

def get_questions():
    questions = {}
    result = []
    with open(QUESTIONS) as file:
        for row in file:
            record = row.split(",")
            for i in range(len(record)):
                questions[QUESTIONS_HEADERS[i]] = record[i]
            result.append(questions)
        return result

def get_details():

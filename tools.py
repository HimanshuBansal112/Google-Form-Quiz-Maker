import os
import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Making_Q_and_A_Form")

file_path = "form.json"
req_mcq = 15
req_multi = 3
req_blank = 2


def create_if_not_exist():
    if not os.path.exists(file_path):
        default_json = {
            "mcq": 0,
            "multi_choice": 0,
            "fill_in_blank": 0,
            "next_id": 0,
            "data": [
                {
                    "updateSettings": {
                        "settings": {"quizSettings": {"isQuiz": True}},
                        "updateMask": "quizSettings.isQuiz",
                    }
                }
            ],
        }
        with open(file_path, "w") as f:
            json.dump(default_json, f, indent=2)


def save(data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def load():
    create_if_not_exist()
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


@mcp.tool(name="instructions", description="Instructions to avoid past mistakes.")
def instructions() -> str:
    return """
    1. Do not include any form of question numbering/labeling,
    such as Q1, Q-1, Q, or similar formats.
    2. Title of question cannot contain newlines.
    3. Title should be like what is the output?, what is correct?, etc. No hint, no question number in title.
    4. You can make description empty if not needed or if redundant.
    5. It doesn't support formatting using backtick or bold or any such. Description can have newlines.
    """


@mcp.tool(
    name="check_remaining",
    description="Returns how many MCQ, multi-choice, and fill-in-the-blank questions can still be added.",
)
def check_remaining() -> dict:
    data = load()
    counts = {"mcq": 0, "multi_choice": 0, "fill_in_blank": 0}
    counts["mcq"] = max(0, req_mcq - data["mcq"])
    counts["multi_choice"] = max(0, req_multi - data["multi_choice"])
    counts["fill_in_blank"] = max(0, req_blank - data["fill_in_blank"])
    return counts


@mcp.tool(
    name="add_mcq",
    description="Adds a multiple choice question with exactly 4 options, one correct answer, and explanations.",
)
def add_mcq(
    question_title: str,
    question_description: str,
    options: list[str],
    correct_option_index: int,
    correct_option_explanation: str,
    incorrect_option_explanation: str,
):
    data = load()
    if data["mcq"] > req_mcq - 1:
        return f"More than {req_mcq} MCQs are not allowed."
    if len(options) != 4:
        return "Failed! Options should be of length 4."
    if correct_option_index > 3 or correct_option_index < 0:
        return "Invalid index! It should be 0-3."
    if len(correct_option_explanation) > 600:
        return "Overflow of correct option explanation!!! Size of explanation should be below 600 characters."
    if len(incorrect_option_explanation) > 600:
        return "Overflow of incorrect option explanation!!! Size of explanation should be below 600 characters."
    if len(question_description) > 300:
        return (
            "Overflow of question description!!! Size of question description should be below 300 characters."
        )
    if len(question_title) > 100:
        return (
            "Overflow of question title!!! Size of question title should be below 100 characters."
        )

    values = {
        "createItem": {
            "location": {"index": data["next_id"]},
            "item": {
                "title": question_title,
                "description": question_description,
                "questionItem": {
                    "question": {
                        "required": True,
                        "grading": {
                            "pointValue": 1,
                            "correctAnswers": {
                                "answers": [{"value": options[correct_option_index]}]
                            },
                            "whenRight": {"text": correct_option_explanation},
                            "whenWrong": {"text": incorrect_option_explanation},
                        },
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [{"value": option} for option in options],
                        },
                    }
                },
            },
        }
    }
    data["data"].append(values)
    data["mcq"] += 1
    data["next_id"] += 1
    save(data)
    return "MCQ added successfully"


@mcp.tool(
    name="add_multi_choice",
    description="Adds a multi-choice question with 4 options and one or more correct answers.",
)
def add_multi_choice(
    question_title: str,
    question_description: str,
    options: list[str],
    correct_options_index: list[int],
    general_explanation: str,
):
    data = load()
    if data["multi_choice"] > req_multi - 1:
        return f"More than {req_multi} multi-choice are not allowed."
    if len(options) != 4:
        return "Failed! Options should be of length 4."
    if len(correct_options_index) < 1:
        return "Invalid count! There should be 1-4 correct options."
    for index in correct_options_index:
        if index > 3 or index < 0:
            return "Invalid index! It should be 0-3."
    if len(general_explanation) > 600:
        return "Overflow of correct option general_explanation!!! Size of general_explanation should be below 600 characters."
    if len(question_description) > 300:
        return (
            "Overflow of question description!!! Size of question description should be below 300 characters."
        )
    if len(question_title) > 100:
        return (
            "Overflow of question title!!! Size of question title should be below 100 characters."
        )

    values = {
        "createItem": {
            "location": {"index": data["next_id"]},
            "item": {
                "title": question_title,
                "description": question_description,
                "questionItem": {
                    "question": {
                        "required": True,
                        "grading": {
                            "pointValue": 1,
                            "correctAnswers": {
                                "answers": [
                                    {"value": options[correct]}
                                    for correct in correct_options_index
                                ]
                            },
                            "whenRight": {"text": general_explanation},
                            "whenWrong": {"text": general_explanation},
                        },
                        "choiceQuestion": {
                            "type": "CHECKBOX",
                            "options": [{"value": option} for option in options],
                        },
                    }
                },
            },
        }
    }
    data["data"].append(values)
    data["multi_choice"] += 1
    data["next_id"] += 1
    save(data)
    return "Multi-choice added successfully"


@mcp.tool(
    name="add_blank",
    description="Adds a fill-in-the-blank question with similar matching correct answer and explanation.",
)
def add_blank(
    question_title: str,
    question_description: str,
    answers: list[str],
    general_explanation: str
):
    data = load()
    if data["fill_in_blank"] > req_blank - 1:
        return f"More than {req_blank} Fill-in Blanks are not allowed."
    if len(general_explanation) > 600:
        return "Overflow of correct option general_explanation!!! Size of general_explanation should be below 600 characters."
    if len(question_description) > 300:
        return (
            "Overflow of question description!!! Size of question description should be below 300 characters."
        )
    if len(question_title) > 100:
        return (
            "Overflow of question title!!! Size of question title should be below 100 characters."
        )
    if len(answers) == 0:
        return "Empty answer not allowed."
    for answer in answers:
        if len(answer) > 50:
            return "Overflow of answer!!! Size of answer should be below 50 characters."

    values = {
        "createItem": {
            "location": {"index": data["next_id"]},
            "item": {
                "title": question_title,
                "description": question_description,
                "questionItem": {
                    "question": {
                        "required": True,
                        "grading": {
                            "pointValue": 1,
                            "correctAnswers": {
                                "answers": [{"value": answer} for answer in answers]
                            },
                            "generalFeedback": {"text": general_explanation},
                        },
                        "textQuestion": {"paragraph": False},
                    }
                },
            },
        }
    }

    data["data"].append(values)
    data["fill_in_blank"] += 1
    data["next_id"] += 1
    save(data)
    return "Fill-in Blank added successfully"


if __name__ == "__main__":
    mcp.run()

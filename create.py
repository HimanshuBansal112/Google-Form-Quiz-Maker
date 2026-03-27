from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import json

SCOPES = ['https://www.googleapis.com/auth/forms.body']

file_path = "form.json"
def load():
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def prepare(data):
    for i in range(1, len(data["data"])):
        data["data"][i]["createItem"]["item"]["title"] = f"Q-{i} " + data["data"][i]["createItem"]["item"]["title"]
    return data

def main(title, description):
    data = load()
    data = prepare(data)
    if "data" not in data or not isinstance(data["data"], list):
        print("Invalid form.json structure.")
        return
    if len(data["data"]) <= 1:
        print("No questions to add.")
        return
    if len(data["data"]) > 100:
        print("Too many requests. Split into batches.")
        return
    creds = None
    if os.path.exists('forms_token.pickle'):
        with open('forms_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('forms_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    form_service = build('forms', 'v1', credentials=creds)

    form_info = {
        "info": {
            "title": title,
            "documentTitle": title
        }
    }
    created_form = form_service.forms().create(body=form_info).execute()
    form_id = created_form.get('formId')
    print(f"Form created! ID: {form_id}")

    update_request = {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {
                        "description": description
                    },
                    "updateMask": "description"
                }
            }
        ] + data["data"]
    }

    try:
        result = form_service.forms().batchUpdate(
            formId=form_id,
            body=update_request
        ).execute()
    except Exception as e:
        print("Error while updating form:", e)
        return
    print(f"Edit: https://docs.google.com/forms/d/{form_id}/edit")
    print(f"Live: https://docs.google.com/forms/d/{form_id}/viewform")

if __name__ == '__main__':
    title = input("Enter title: ")
    description = input("Enter description: ")
    main(title, description)
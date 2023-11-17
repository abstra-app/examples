import os, unittest
# from e2e.tests import TestExamples
from datetime import datetime
from dotenv import load_dotenv
from slack_sdk import WebClient

# This hook uses environment variables.
load_dotenv()

now = lambda: str(datetime.timestamp(datetime.now())).split(".")[0]
folder_name = now()
os.environ["FOLDER_NAME"] = folder_name
channel_name = os.environ.get("SLACK_CHANNEL_NAME")
slack_token = os.environ.get("SLACK_BOT_TOKEN")

def slack_msg(msg, files=[]):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    client = WebClient(token=slack_token)

    if files:
        for file in files:
            upload = client.files_upload(file=file, filename=file.split("/")[1])
            msg = msg + "\n" + upload["file"]["permalink"]

    client.chat_postMessage(channel=channel_name, text=msg)


program = unittest.main(exit=False)
if not program.result.wasSuccessful():
    problems = program.result.errors + program.result.failures
    failed_tests = "\n".join([problem[0]._testMethodName for problem in problems])
    files = [f"{folder_name}/{file}" for file in os.listdir(folder_name)]
    slack_msg(":test_tube:  E2E tests: Failing :x: :\n" + failed_tests, files)
    exit(1)  # isso nao funciona
else:
    slack_msg(":test_tube:  E2E tests: Passing :white_check_mark:")
import os
import time
import re
import secrets
from slackclient import SlackClient
from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants


slack_client = SlackClient(secrets.luckycat_access_token)
starterbot_id = None

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
HERE_REGEX = "(.*)<(!here)>(.*)"
channel = secrets.leftovers_channel

PIN = 9


def wave_arm(board):
    for i in range(4):
        board.analog_write(PIN, 180)
        board.sleep(0.5)
        board.analog_write(PIN, 0)
        board.sleep(0.5)
    board.analog_write(PIN, 92)


def parse_here_mention(message_text):
    matches = re.search(HERE_REGEX, message_text)
    return " ".join([matches.group(1).strip(), matches.group(3).strip()]) if matches else None


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("LuckyCat connected and running!")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]

        board = PyMata3(2)
        board.servo_config(PIN)

        while True:
            for event in slack_client.rtm_read():
                if event["type"] == "message" and not "subtype" in event:
                    food = parse_here_mention(event["text"])
                    if food:
                        print('TASTY LUCKYCAT YUM')
                        print(food)
                        os.system('say "' + food + '"')
                        wave_arm(board)
                    else:
                        print('no food for you')
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

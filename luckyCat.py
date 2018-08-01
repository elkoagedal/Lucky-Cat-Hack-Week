import os
import time
import re
import secrets
from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient(secrets.luckycat_access_token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
HERE_REGEX = "<(!here)>"
channel = secrets.leftovers_channel

def has_here_mention(message_text):
    matches = re.search(HERE_REGEX, message_text)
    return bool(matches)


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("LuckyCat connected and running!")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            for event in slack_client.rtm_read():
                if event["type"] == "message" and not "subtype" in event:
                    if has_here_mention(event["text"]):
                        print('TASTY LUCKYCAT YUM')
                    else:
                        print('no food for you')
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

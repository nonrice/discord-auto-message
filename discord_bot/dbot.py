from http.client import HTTPSConnection
from sys import stderr
from json import dumps
from time import sleep
from random import random

file = open("info.txt")
text = file.read().splitlines()

if len(text) != 4 or input("Configure bot? (y/n)") == "y":
    if len(text) != 4:
        print("An error was found inside the info file (possibly your first time using?), reconfiguring is required.")
    print("Refer to Google if some of these parameters are unfamiliar. It should yield more than usable results.")
    file.close()
    file = open("info.txt", "w")
    text = []
    text.append(input("User agent: "))
    text.append(input("Discord token: "))
    text.append(input("Discord channel URL: "))
    text.append(input("Discord channel ID: "))

    for parameter in text:
        file.write(parameter + "\n")

    file.close()



header_data = {
    "content-type": "application/json",
    "user-agent": text[0],
    "authorization": text[1],
    "host": "discordapp.com",
    "referrer": text[2]
}

print("Messages will be sent to " + header_data["referrer"] + ".")

def get_connection():
    return HTTPSConnection("discordapp.com", 443)


def send_message(conn, channel_id, message_data):
    try:
        conn.request("POST", f"/api/v6/channels/{channel_id}/messages", message_data, header_data)
        resp = conn.getresponse()

        if 199 < resp.status < 300:
            print("Message sent!")
            pass

        else:
            stderr.write(f"Received HTTP {resp.status}: {resp.reason}\n")
            pass

    except:
        stderr.write("Failed to send_message\n")
        for key in header_data:
            print(key + ": " + header_data[key])


def main(msg):
    message_data = {
        "content": msg, # message goes here
        "tts": "false",
    }

    send_message(get_connection(), text[3], dumps(message_data))


if __name__ == '__main__':
    message = input("Message to send: ")
    messages = int(input("Amount of messages: "))
    main_wait = int(input("Seconds between messages: "))
    human_margin = int(input("Human error margin: "))

    for i in range(0,messages):
        main(message)
        print("Estimated time to complete: " + str((messages-i) * (human_margin // 2 + main_wait) // 60) + " minutes.")
        print("Iteration " + str(i) + " complete.")
        sleep(main_wait)
        sleep(random()*human_margin)

    print("Session complete! " + str(messages) + " messages sent.")

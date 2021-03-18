from http.client import HTTPSConnection
from sys import stderr
from json import dumps
from time import sleep
from datetime import datetime



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

def connect():
    return HTTPSConnection("discordapp.com", 443)

def send_message(conn, channel_id, message):
    message_data = {
        "content": message,
        "tts": False
    }

    try:
        conn.request("POST", f"/api/v6/channels/{channel_id}/messages", dumps(message_data), header_data)
        resp = conn.getresponse()
        if 199 < resp.status < 300:
            pass
        else:
            stderr.write(f"While sending message, received HTTP {resp.status}: {resp.reason}\n")
            pass
    except:
        stderr.write("Failed to send_message\n")

def check_embed(conn, channel_id, target):

    channel = conn.request("GET", f"/api/v6/channels/{channel_id}/messages", headers=header_data)
    resp = conn.getresponse()

    if 199 < resp.status < 300:
        resp_string = str(resp.read(500))
        if target in resp_string:
            return True
        return False
    else:
        stderr.write(f"While checking message, received HTTP {resp.status}: {resp.reason}\n")
        pass

def cycle(route, target_pk, catch_move_id, kill_move_id, ball_name, box_id):
    sleep(2)
    send_message(connect(), text[3], (".route " + route))
    sleep(1)

    if check_embed(connect(), text[3], target_pk):
        send_message(connect(), text[3], catch_move_id)
        sleep(7)

        while check_embed(connect(), text[3], target_pk):
            send_message(connect(), text[3], ball_name)
            sleep(7)

        print("Caught a " + target_pk + "! " + (datetime.now()).strftime("%H:%M:%S"))
        send_message(connect(), text[3], (".boxswap " + box_id + " " + target_pk))
        return True

    else:
        send_message(connect(), text[3], kill_move_id)
        return False

def main():
    pokemon = input("Pokemon to catch: ")
    ball = input("Ball to use: ")
    box = input("Box to store Pokemon: ")
    route = input("Pokemon route: ")
    amount = input("Amount of this pokemon to catch: ")

    print("Looking for " + pokemon + "... " + (datetime.now()).strftime("%H:%M:%S"))
    counter = 0
    while counter < int(amount):
        if cycle(route, pokemon, "1", "4", ball, box):
            counter += 1

    print("Finished catching " + amount + " " + pokemon + "! " + (datetime.now()).strftime("%H:%M:%S"))

main()

import hashlib
import random
import requests
import json
import time
import sys
from timeit import default_timer as timer

from cpu import CPU

from util import Stack, Queue

full_data = {}
lambda_url = "https://lambda-treasure-hunt.herokuapp.com/api"
api_key = ""

with open("./export.json", "r") as file:
    full_data = json.loads(file.read())

headers = { 'Authorization': "Token " + api_key }
r = requests.get(lambda_url + "/adv/init/", headers = headers)

current_room = r.json()

def proof_of_work(last_proof, difficulty):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    proof = random.randrange(50000, 10000000)

    #  TODO: Your code here
    while valid_proof(last_proof, proof, difficulty) is False:
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof

def valid_proof(last_proof, proof, difficulty):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # TODO: Your code here!

    guess = f"{last_proof}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:difficulty] == ("0" * difficulty)

def bfs(current_room, next_room):
    visited = {}

    q = Queue()
    q.enqueue( [current_room] )

    while next_room not in visited:
        path = q.dequeue()
        current_room = str(path[-1])

        if current_room not in visited:
            visited[str(current_room)] = path

            for direction in full_data[str(current_room)]['directions']:
                new_path = path.copy()
                new_path.append(full_data[str(current_room)]['directions'][direction])

                q.enqueue(new_path)

    return visited[next_room]

def travel(direction, next_room_id = None):
    while True:
        data = None
        post_info = { 'direction': direction }

        if next_room_id is not None:
            post_info['next_room_id'] = str(next_room_id)

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        print(f"Traveling {direction}: {next_room_id}")

        try:
            r = requests.post(url=lambda_url + "/adv/move/", data=json.dumps(post_info), headers = headers)

            data = r.json()

            r.raise_for_status()
            print(f"Items: {data['items']} in {next_room_id}")
            print(f"Messages: {data['messages']}")
            print(f"Moved: sleeping for {data['cooldown']}")

            time.sleep(data['cooldown'])

            return data
        except:
            print(data)
            print(f"Error: resuming in {data['cooldown'] + 5}")
            time.sleep(data['cooldown'] + 5)

def travel_dash(direction, num_rooms, next_room_ids):
    while True:
        data = None
        post_info = { 'direction': direction, 'num_rooms': str(num_rooms), 'next_room_ids': next_room_ids }

        print(json.dumps(post_info))

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        print(f"Dashing {direction}: {next_room_ids}")

        try:
            r = requests.post(url=lambda_url + "/adv/dash/", data=json.dumps(post_info), headers = headers)

            data = r.json()

            r.raise_for_status()

            print(f"Dashed: Waiting {data['cooldown']}")

            time.sleep(data['cooldown'])

            return data
        except:
            print(r.text)
            print(f"Error: resuming in {data['cooldown'] + 5}")
            time.sleep(data['cooldown'] + 5)

directions = ['n', 's', 'e', 'w']

while True:
    print()
    print(current_room)
    print(f"You are in room: {current_room['title']}({current_room['room_id']}): {current_room['description']}")
    print(f"Items in room: {current_room['items']}")
    print(f"With exits to {full_data[str(current_room['room_id'])]['directions']}")

    command = input("> ")

    words = command.split(" ")
    command = words[0]
    words = words[1:]
    
    if command == "q":
        break
    elif command == "n":
        current_room = travel("n")
    elif command == "s":
        current_room = travel("s")
    elif command == "e":
        current_room = travel("e")
    elif command == "w":
        current_room = travel("w")
    elif command == "travel":
        path_to = bfs(current_room['room_id'], words[0])[1:]

        print(path_to)

        for room in path_to:
            for direc in directions:
                if direc in full_data[str(current_room['room_id'])]['directions'] and full_data[str(current_room['room_id'])]['directions'][direc] == room:
                    current_room = travel(direc, full_data[str(current_room['room_id'])]['directions'][direc])  

    elif command == "pickup":
        print(" ".join([x for x in words]))
        post_info = { "name": " ".join([x for x in words]) }

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/take/", data=json.dumps(post_info), headers = headers)

        result = r.json()

        print()

        print(result)
    elif command == "recall":
        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/recall/", headers = headers)

        result = r.json()

        current_room = result

        print()

        print(result)
    elif command == "sell":
        post_info = { "name": "treasure" }

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/sell/", data=json.dumps(post_info), headers = headers)

        result = r.json()

        print()

        print(result)

        print()
    elif command == "confirm":
        post_info = { "name": "treasure", "confirm": "yes" }

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/sell/", data=json.dumps(post_info), headers = headers)

        result = r.json()

        print()

        print(result)

        print()
    elif command == "status":

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/status/", headers = headers)

        result = r.json()

        print()

        print(result)
    elif command == "trans":
        print(" ".join([x for x in words]))
        post_info = { "name": " ".join([x for x in words]) }

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/transmogrify/", data=json.dumps(post_info), headers = headers)

        print()

        print(r.text)

        print()
    elif command == "wear":
        print(" ".join([x for x in words]))
        post_info = { "name": " ".join([x for x in words]) }

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/wear/", data=json.dumps(post_info), headers = headers)

        print()

        print(r.text)

        print()
    elif command == "undress":
        print(" ".join([x for x in words]))
        post_info = { "name": " ".join([x for x in words]) }

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/undress/", data=json.dumps(post_info), headers = headers)

        print()

        print(r.text)

        print()
    elif command == "change":
        print(" ".join([x for x in words]))
        post_info = { "name": " ".join([x for x in words]) }

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/change_name/", data=json.dumps(post_info), headers = headers)

        result = r.json()

        print()

        print(result)

        print()
    elif command == "change_confirm":
        print(" ".join([x for x in words]))
        post_info = { "name": " ".join([x for x in words]), "confirm": "aye" }

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/change_name/", data=json.dumps(post_info), headers = headers)

        result = r.json()

        print()

        print(result)

        print()
    elif command == "pray":

        headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

        r = requests.post(url=lambda_url + "/adv/pray/", headers = headers)

        result = r.json()

        print()

        print(result)

        print()
    elif command == "mine":
        while True:
            if current_room['room_id'] != 55:
                print("Traveling to well")

                path_to = bfs(current_room['room_id'], str(55))[1:]

                print(path_to)
                
                for room in path_to:
                    for direc in directions:
                        if direc in full_data[str(current_room['room_id'])]['directions'] and full_data[str(current_room['room_id'])]['directions'][direc] == room:
                            current_room = travel(direc, full_data[str(current_room['room_id'])]['directions'][direc])

            print("In well")

            post_info = { "name": "WELL" }

            headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

            r = requests.post(url=lambda_url + "/adv/examine/", data=json.dumps(post_info), headers = headers)

            result = r.json()

            print()

            text = result['description']

            print(result)

            print()

            lines = text.split("\n")[2:]

            cpu2 = CPU()
            cpu2.load(lines)
            cpu2.run()

            room_id = ""

            for char in cpu2.output:
                if(char.isdigit()):
                    room_id += char

            path_to = bfs(current_room['room_id'], room_id)[1:]

            print(path_to)
            
            for room in path_to:
                for direc in directions:
                    if direc in full_data[str(current_room['room_id'])]['directions'] and full_data[str(current_room['room_id'])]['directions'][direc] == room:
                        current_room = travel(direc, full_data[str(current_room['room_id'])]['directions'][direc])

            print("In mining room")

            while True:
                last_proof = {}

                post_info = { "name": "WELL" }

                headers = { 'Authorization': "Token " + api_key }

                r = requests.get(url=lambda_url + "/bc/last_proof/", headers = headers)

                result = r.json()

                print(result)

                last_proof = result['proof']
                difficulty = result['difficulty']

                print(f"Last Proof: {last_proof}, Difficulty: {difficulty}")

                new_proof = proof_of_work(last_proof, difficulty)

                print(f"New proof found: {new_proof}")

                post_info = { "proof": new_proof }

                headers = { 'Authorization': "Token " + api_key, 'Content-Type': 'application/json' }

                r = requests.post(url=lambda_url + "/bc/mine/", data=json.dumps(post_info), headers = headers)

                result = r.json()

                print(result)

                time.sleep(result['cooldown'])

                if len(result['errors']) == 0:
                    break

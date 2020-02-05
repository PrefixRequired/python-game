import requests
import time
import json
import sys

from util import Stack, Queue

graph = {0: {'n': '?', 's': 2, 'e': 4, 'w': 1}, 1: {'e': 0}, 4: {'n': 23, 'e': 13, 'w': 0}, 13: {'e': 15, 'w': 4}, 15: {'w': 13}, 23: {'s': 4, 'e': 26}, 26: {'e': 55, 'w': 23}, 55: {'w': 26}, 2: {'n': 0, 's': 6, 'e': 3}, 3: {'s': 9, 'e': 5, 'w': 2}, 5: {'w': 3}, 9: {'n': 3, 's': 12, 'e': 11}, 11: {'e': 17, 'w': 9}, 17: {'n': 24, 'e': 42, 'w': 11}, 42: {'n': 44, 's': 80, 'e': 118, 'w': 17}, 118: {'e': 137, 'w': 42}, 137: {'w': 118}, 80: {'n': 42, 's': 81, 'e': 86}, 86: {'s': 96, 'e': 90, 'w': 80}, 90: {'e': 178, 'w': 86}, 178: {'n': 209, 'e': 243, 'w': 90}, 243: {'s': 293, 'e': 256, 'w': 178}, 256: {'s': 360, 'e': 327, 'w': 243}, 327: {'e': 427, 'w': 256}, 427: {'e': 430, 'w': 327}, 430: {'n': 443, 'e': 439, 'w': 427}, 439: {'w': 430}, 443: {'s': 430, 'e': 471}, 471: {'w': 443}, 360: {'n': 256, 'e': 398}, 398: {'e': 438, 'w': 360}, 438: {'e': 465, 'w': 398}, 465: {'e': 498, 'w': 438}, 498: {'w': 465}, 293: {'n': 243}, 209: {'s': 178}, 96: {'n': 86, 'e': 97}, 97: {'e': 181, 'w': 96}, 181: {'w': 97}, 81: {'n': 80}, 44: {'s': 42}, 24: {'s': 17}, 12: {'n': 9, 's': 18, 'e': 14, 'w': 21}, 21: {'e': 12, 'w': 29}, 29: {'s': 45, 'e': 21, 'w': 49}, 49: {'s': 79, 'e': 29, 'w': 136}, 136: {'e': 49, 'w': 148}, 148: {'e': 136, 'w': 292}, 292: {'n': 301, 'e': 148}, 301: {'n': 304, 's': 292}, 304: {'s': 301}, 79: {'n': 49}, 45: {'n': 29, 's': 60}, 60: {'n': 45, 'e': 36, 'w': 70}, 70: {'s': 163, 'e': 60, 'w': 98}, 98: {'n': 102, 's': 126, 'e': 70, 'w': 109}, 109: {'s': 185, 'e': 98, 'w': 175}, 175: {'s': 183, 'e': 109, 'w': 179}, 179: {'s': 233, 'e': 175, 'w': 213}, 213: {'e': 179, 'w': 420}, 420: {'s': 444, 'e': 213, 'w': 437}, 437: {'e': 420, 'w': 497}, 497: {'e': 437}, 444: {'n': 420, 'w': 490}, 490: {'e': 444, 'w': 493}, 493: {'e': 490}, 233: {'n': 179, 'w': 238}, 238: {'e': 233}, 183: {'n': 175, 's': 229}, 229: {'n': 183, 's': 250, 'w': 236}, 236: {'s': 264, 'e': 229}, 264: {'n': 236, 's': 274, 'w': 273}, 273: {'n': 343, 'e': 264}, 343: {'s': 273, 'w': 351}, 351: {'s': 491, 'e': 343, 'w': 478}, 478: {'e': 351}, 491: {'n': 351}, 274: {'n': 264, 'w': 308}, 308: {'e': 274}, 250: {'n': 229, 's': 294, 'e': 289}, 289: {'w': 250}, 294: {'n': 250, 's': 334}, 334: {'n': 294, 's': 393, 'e': 341, 'w': 391}, 391: {'s': 396, 'e': 334, 'w': 428}, 428: {'e': 391}, 396: {'n': 391}, 341: {'s': 449, 'w': 334}, 449: {'n': 341}, 393: {'n': 334, 's': 482}, 482: {'n': 393}, 185: {'n': 109}, 126: {'n': 98, 's': 129}, 129: {'n': 126, 'e': 194, 'w': 170}, 170: {'e': 129}, 194: {'s': 214, 'w': 129}, 214: {'n': 194, 'e': 173, 'w': 226}, 226: {'s': 300, 'e': 214}, 300: {'n': 226, 's': 377, 'w': 389}, 389: {'e': 300}, 377: {'n': 300}, 173: {'e': 133, 'w': 214}, 133: {'e': 117, 'w': 173}, 117: {'n': 108, 's': 131, 'e': 166, 'w': 133}, 166: {'s': 198, 'e': 150, 'w': 117}, 150: {'n': 135, 'w': 166}, 135: {'s': 150, 'e': 106}, 106: {'n': 100, 's': 111, 'w': 135}, 111: {'n': 106, 's': 367, 'e': 158}, 158: {'s': 167, 'w': 111}, 167: {'n': 158, 's': 262, 'e': 260}, 260: {'w': 167}, 262: {'n': 167, 's': 370, 'e': 358}, 358: {'e': 401, 'w': 262}, 401: {'w': 358}, 370: {'n': 262, 's': 434, 'e': 407}, 407: {'s': 496, 'w': 370}, 496: {'n': 407}, 434: {'n': 370}, 367: {'n': 111}, 100: {'s': 106, 'e': 112, 'w': 68}, 68: {'n': 52, 'e': 100}, 52: {'n': 35, 's': 68, 'e': 75}, 75: {'e': 85, 'w': 52}, 85: {'e': 154, 'w': 75}, 154: {'e': 193, 'w': 85}, 193: {'e': 251, 'w': 154}, 251: {'e': 315, 'w': 193}, 315: {'w': 251}, 35: {'s': 52, 'w': 34}, 34: {'n': 14, 's': 50, 'e': 35}, 50: {'n': 34, 's': 89}, 89: {'n': 50, 's': 93}, 93: {'n': 89, 'w': 108}, 108: {'n': 78, 's': 117, 'e': 93}, 131: {'n': 117, 's': 244, 'w': 138}, 138: {'s': 211, 'e': 131, 'w': 195}, 195: {'s': 228, 'e': 138, 'w': 225}, 225: {'s': 278, 'e': 195}, 278: {'n': 225}, 228: {'n': 195, 's': 281}, 281: {'n': 228, 's': 318, 'e': 309, 'w': 317}, 317: {'s': 387, 'e': 281, 'w': 409}, 409: {'e': 317}, 387: {'n': 317, 's': 417, 'w': 431}, 431: {'e': 387, 'w': 492}, 492: {'e': 431}, 417: {'n': 387}, 309: {'s': 333, 'e': 326, 'w': 281}, 326: {'s': 342, 'w': 309}, 342: {'n': 326, 's': 432}, 432: {'n': 342}, 333: {'n': 309, 's': 378}, 378: {'n': 333}, 318: {'n': 281, 's': 487}, 487: {'n': 318, 's': 489}, 489: {'n': 487}, 211: {'n': 138}, 244: {'n': 131, 'e': 239}, 239: {'n': 198, 'w': 244}, 198: {'n': 166, 's': 239, 'e': 199}, 199: {'s': 230, 'w': 198}, 230: {'n': 199, 's': 307, 'e': 297}, 297: {'w': 230}, 307: {'n': 230, 's': 373, 'e': 371, 'w': 321}, 321: {'s': 413, 'e': 307}, 413: {'n': 321}, 371: {'s': 475, 'w': 307}, 475: {'n': 371, 's': 484}, 484: {'n': 475}, 373: {'n': 307, 's': 480}, 480: {'n': 373}, 78: {'n': 22, 's': 108}, 22: {'n': 18, 's': 78, 'w': 36}, 36: {'s': 48, 'e': 22, 'w': 60}, 48: {'n': 36, 's': 105, 'w': 149}, 149: {'e': 48}, 105: {'n': 48, 'w': 202}, 202: {'e': 105}, 18: {'n': 12, 's': 22, 'w': 25}, 25: {'e': 18}, 14: {'s': 34, 'e': 37, 'w': 12}, 37: {'w': 14}, 112: {'s': 141, 'e': 140, 'w': 100}, 140: {'w': 112}, 141: {'n': 112, 'e': 156}, 156: {'s': 168, 'e': 164, 'w': 141}, 164: {'n': 217, 'e': 298, 'w': 156}, 298: {'s': 324, 'w': 164}, 324: {'n': 298, 's': 349, 'e': 354}, 354: {'w': 324}, 349: {'n': 324, 's': 352, 'e': 384, 'w': 356}, 356: {'e': 349}, 384: {'w': 349}, 352: {'n': 349, 's': 362, 'e': 485}, 485: {'w': 352}, 362: {'n': 352, 's': 399, 'w': 463}, 463: {'s': 468, 'e': 362}, 468: {'n': 463}, 399: {'n': 362, 's': 467}, 467: {'n': 399}, 217: {'s': 164, 'e': 247}, 247: {'e': 261, 'w': 217}, 261: {'s': 277, 'e': 322, 'w': 247}, 322: {'n': 382, 'e': 435, 'w': 261}, 435: {'w': 322}, 382: {'s': 322, 'e': 388}, 388: {'e': 477, 'w': 382}, 477: {'e': 483, 'w': 388}, 483: {'w': 477}, 277: {'n': 261, 'e': 323}, 323: {'e': 433, 'w': 277}, 433: {'s': 455, 'e': 460, 'w': 323}, 460: {'w': 433}, 455: {'n': 433}, 168: {'n': 156, 'e': 340}, 340: {'w': 168}, 102: {'s': 98, 'w': 142}, 142: {'e': 102, 'w': 159}, 159: {'e': 142, 'w': 196}, 196: {'n': 222, 'e': 159, 'w': 197}, 197: {'n': 232, 'e': 196, 'w': 276}, 276: {'e': 197, 'w': 419}, 419: {'e': 276}, 232: {'n': 272, 's': 197, 'w': 235}, 235: {'n': 330, 'e': 232, 'w': 355}, 355: {'e': 235}, 330: {'n': 369, 's': 235, 'w': 383}, 383: {'e': 330, 'w': 495}, 495: {'e': 383}, 369: {'n': 400, 's': 330, 'w': 376}, 376: {'e': 369}, 400: {'s': 369}, 272: {'n': 295, 's': 232}, 295: {'s': 272}, 222: {'n': 305, 's': 196}, 305: {'n': 365, 's': 222}, 365: {'s': 305}, 163: {'n': 70}, 6: {'n': 2, 'w': 7}, 7: {'n': 8, 'e': 6, 'w': 56}, 56: {'e': 7, 'w': 61}, 61: {'e': 56, 'w': 171}, 171: {'e': 61}, 8: {'s': 7, 'w': 16}, 16: {'n': 58, 'e': 8, 'w': 67}, 162: {'e': 67}, 67: {'e': 16, 'w': 162}, 58: {'s': 16, 'w': 65}, 65: {'n': 74, 'e': 58, 'w': 139}, 139: {'e': 65, 'w': 188}, 188: {'e': 139, 'w': 335}, 335: {'e': 188, 'w': 366}, 366: {'e': 335}, 74: {'n': 87, 's': 65, 'w': 161}, 161: {'e': 74}, 87: {'s': 74}}
player_dict = {}
visited_rooms = set()
lambda_url = "https://lambda-treasure-hunt.herokuapp.com/api"

with open("info.txt", "r") as file:
    lines = file.readlines()

    for line in lines:
        info = line.split("=")
        key = info[0]
        value = info[1]
        
        player_dict[key] = value

headers = { 'Authorization': "Token " + player_dict["api_key"] }
r = requests.get(lambda_url + "/adv/init/", headers = headers)

data = r.json()

time.sleep(10)

def bfs(current_room, next_room):
    visited = {}

    q = Queue()
    q.enqueue( [current_room] )

    while next_room not in visited:
        path = q.dequeue()
        current_room = path[-1]

        if current_room not in visited:
            visited[current_room] = path

            for direction in graph[current_room]:
                if graph[current_room][direction] != '?':
                    new_path = path.copy()
                    new_path.append(graph[current_room][direction])

                    q.enqueue(new_path)


    return visited[next_room]

def reverse(direction):
    if direction is 'n':
        return 's'
    elif direction is 's':
        return 'n'
    elif direction is 'e':
        return 'w'
    elif direction is 'w':
        return 'e'

def traverse_maze(data_received):
    directions = ['n', 's', 'e', 'w']
    final_path = []

    current_room = data_received
    current_id = current_room['room_id']

    unvisited = Stack()
    last_room = (0,'direction')

    path_to_next = bfs(current_id, 0)[1:]
            
    for room in path_to_next:
        for direc in directions:
            if direc in graph[current_id] and graph[current_id][direc] == room:
                last_room = (current_id, reverse(direc))

                current_room = travel(direc)

                final_path.append(direc)

    while True:
        current_id = current_room['room_id']
        print(f"In room {current_id}")
        print(graph)
        # if current room isnt in the graph, put it in with '?' and connect the previous room to this one and vice versa
        # else the current room is already in, set the last rooms direction towards the current room to the current room
        if current_id not in graph:
            graph[current_id] = {}
            for direction in current_room['exits']:
                if direction == last_room[1]:
                    graph[last_room[0]][reverse(last_room[1])] = current_id
                    graph[current_id][direction] = last_room[0]
                else:
                    graph[current_id][direction] = '?'
        else:
            graph[last_room[0]][reverse(last_room[1])] = current_id
            graph[current_id][last_room[1]] = last_room[0]

        # if the room hasnt been visited yet, add all of its directions that have a '?' to the stack
        if json.dumps(current_room) not in visited_rooms:
            for direc in directions:
                if direc in graph[current_id] and graph[current_id][direc] == '?':
                    unvisited.push( (current_id, direc) )

        visited_rooms.add(json.dumps(current_room))
        next_room = unvisited.pop()

        # stack was empty, return final path
        if next_room is None:
            return final_path

        last_room = (current_id, reverse(next_room[1]))

        # if were in the next room just travel there
        # else do a bfs to find a path to the next '?', and convert all rooms to directions and travel at the same time
        if current_id == next_room[0]:
            current_room = travel(next_room[1])
            final_path.append(next_room[1])
        else:
            path_to_next = bfs(current_id, next_room[0])[1:]
            
            for room in path_to_next:
                for direc in directions:
                    if direc in graph[current_id] and graph[current_id][direc] == room:
                        last_room = (current_id, reverse(direc))

                        current_room = travel(direc)

                        final_path.append(direc)
                
            unvisited.push(next_room)

        if len(visited_rooms) == 500:
            return final_path

def travel(direction, next_room_id = None):
    while True:
        data = None
        post_info = { 'direction': direction }

        if next_room_id is not None:
            post_info['next_room_id'] = next_room_id

        headers = { 'Authorization': "Token " + player_dict["api_key"], 'Content-Type': 'application/json' }

        print(f"Traveling {direction}")

        try:
            r = requests.post(url=lambda_url + "/adv/move/", data=json.dumps(post_info), headers = headers)

            data = r.json()

            print(r.text)

            r.raise_for_status()

            f = open("data.json", "a")
            f.write(json.dumps(data) + ",")
            f.close()

            print(data)

            time.sleep(data['cooldown'] + 2)

            return data
        except:
            print(f"Error: resuming in {data['cooldown'] + 15}")
            time.sleep(data['cooldown'] + 15)

        

def begin_traversal(data):
    arr = traverse_maze(data)
    print(arr)

    f = open("result.txt", "w")
    f.write(arr)
    f.close()

def move_player_direction():
    pass

print(data)

begin_traversal(data)
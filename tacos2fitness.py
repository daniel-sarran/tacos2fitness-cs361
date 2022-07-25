#
#   tacos2fitness server in Python
#   Binds REP socket to tcp://*:6666
#   Expects 
#       b"X lb"
#   from client, replies with 
#       b"{Number of tacos that represents}"
#
#   Expects 
#       b"X cal"
#   from client, replies with 
#       b"{Taco options that are under that calorie limit}"

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:6666")

TACOS = {
        "adobada taco": 400,
        "al pastor taco": 350,
        "carne asada taco": 250,
        }

def tacos_under_limit(limit):
    cal_limit = int(limit)
    result = dict(filter(lambda taco: taco[1] < cal_limit, TACOS.items()))
    tacos_under_limit = [
            f'{taco[0]}:{taco[1]}' 
            for taco 
            in result.items()
            ]
    response = (",").join(tacos_under_limit)
    return response


def weight_to_tacos(weight):
    weight = int(weight)
    num_tacos = weight * 4
    return f"If you deadlift {weight} pounds, you could deadlift {num_tacos} tacos"

    
def main():
    while True:
        #  Wait for next request from client
        message = socket.recv()
        print(f"Received request: {message}")

        message = message.decode('UTF-8')
        params = message.split(' ')

        # If I deadlift 400 lbs, how many tacos could I deadlift?
        if params[1] == 'lb':
            weight = params[0]
            response = weight_to_tacos(weight)

        # Which tacos can I eat under X calories?
        elif params[1] == 'cal':
            limit = params[0]
            response = tacos_under_limit(limit)

        #  Send reply back to client
        socket.send_string(response)

if __name__ == '__main__':
    main()

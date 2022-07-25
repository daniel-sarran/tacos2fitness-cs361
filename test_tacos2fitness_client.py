#
#   Test tacos2fitness client in Python
#   Connects REQ socket to tcp://localhost:6666
#   Sends "X lb" or "X cal" to server
#   Expects {number of tacos you can deadlift} or {taco options under cal}
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to tacos2fitness server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:6666")

requests = ["400 cal", "300 cal", "350 lb", "400 lb"]
for request in requests:
    print(f"Sending request '{request}'...")
    socket.send_string(request)

#  Get the reply.
    message = socket.recv()
    message = message.decode('UTF-8')
    print(f"Received reply:")
    print(f"{message}")

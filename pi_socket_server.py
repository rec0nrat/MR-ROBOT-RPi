#************************************************************************************************************
#   Developer: Tyler Weiss
#   Last Update: 8/18/2016
#
#   SUMMARY: "Mr. Robot" project 
#               Simple socket server that opens a port and waits for connection.
#               Once connection is established SET LED's HIGH and enter
#               command loop. Input stream is processed by the logic loop and
#               if input = "valid CMD" the command is passed to the arduino/motors.
#               A response is sent back to the client device command has been processed.
#               
#
#************************************************************************************************************


import socket   # Client/Server connection
import serial   # Arduino/RPi copnnection
from random import randint
import RPi.GPIO as gpio     # LED control

# SETUP LED GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(24, gpio.OUT)
gpio.setup(25, gpio.OUT)

# Connection Var's
ser = serial.Serial('/dev/ttyUSB0',9600)
host = ''
port = 666

# Awsome-O movie idea collection
movies = ["So what if Adam Sandler, like, had a twin sister, played by Adam Sandler, and um, is seduced by Al Pacino, or something.",
          "So Adam Sandler is a guy who works at a hotel that can make bedtime stories come to life or something.",
          "So what if Adam Sandler is like, in the Israeli special forces, but fakes his own death so he can become a New York stylist, or something..",
          "So Adam Sandler and Kevin James pretend to be gay so they can reciev domestic partner benefits or something..",
          "So Adam Sandler is like the son of Satan, who goes up to Earth and eats chicken or something..",
          "So Whoopie Goldberg is like a detective in the future, who teams up with a dinosaur to stop a mad scientist from destroying the world or something..",
          "So Michaels Keaton is like a dad, who comes back as a snowman, or something.."]

# SETUP comm socket and INIT LED's
def setupServer():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create socket
    print("Socket created")
    try:
        s.bind((host, port))    # bind socket to port
    except socket.error as msg:
        print(msg)
        
    print("Socket bind complete.")

    # LED's start OFF
    gpio.output(24, gpio.LOW)
    gpio.output(25, gpio.LOW)
    
    return s

# Listens for a client connection
def setupConnection():
    s.listen(1)     # allows only one connection
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

# Data processing and logic loop
def dataTransfer(conn):

    # Decode and store client message
    data = conn.recv(1024)
    data = data.decode('UTF-8')
    command = data

    # Check commands list
    if command == 'TURN RIGHT':
        reply = 'Turning right'
        ser.write("right")
        print("Turning Right")
    elif command == 'CONNECT':      # Check the connection from client
        # LED's ON 
        gpio.output(24, gpio.HIGH)
        gpio.output(25, gpio.HIGH)
        reply = 'I am mister robot and I am alive. give me a command.'
        print("It's Alliiiiive!!!")
    elif command == 'TURN LEFT':
        reply = 'Turning left'
        ser.write("left")
        print(reply)
    elif command == 'STOP':
        reply = "Stopping"
        ser.write("stop")
        print("Stopping")
    elif command == 'FORWARD':
        reply = "On the move"
        ser.write("forward")
        print("On the move")
    elif command == 'MOVIE':            # Picks a random crappy movie idea and sends it as reply to client
        reply = movies[randint(0,5)]
    elif command == 'KILL':             # Disconnect from client 
        gpio.output(24, gpio.LOW)
        gpio.output(25, gpio.LOW)
        print("Shutting down")
        reply = "Disconnected"
        conn.sendall(str.encode(reply))
        gpio.cleanup()                  # Close socket connection
        s.close()
    else:
        reply = 'Unknown Commnad'
        print(reply)
        
    conn.sendall(str.encode(reply))     # send reply to client
    print("Data has been sent!")


s = setupServer()   # INIT server

# Continue to process incomming data though socket 
while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        gpio.cleanup()
        break

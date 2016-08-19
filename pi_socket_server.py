import socket
import serial
from random import randint
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(24, gpio.OUT)
gpio.setup(25, gpio.OUT)

ser = serial.Serial('/dev/ttyUSB0',9600)
host = ''
port = 666

storedValue = "whats happpening?!!"

movies = ["So what if Adam Sandler, like, had a twin sister, played by Adam Sandler, and um, is seduced by Al Pacino, or something.",
          "So Adam Sandler is a guy who works at a hotel that can make bedtime stories come to life or something.",
          "So what if Adam Sandler is like, in the Israeli special forces, but fakes his own death so he can become a New York stylist, or something..",
          "So Adam Sandler and Kevin James pretend to be gay so they can reciev domestic partner benefits or something..",
          "So Adam Sandler is like the son of Satan, who goes up to Earth and eats chicken or something..",
          "So Whoopie Goldberg is like a detective in the future, who teams up with a dinosaur to stop a mad scientist from destroying the world or something..",
          "So Michaels Keaton is like a dad, who comes back as a snowman, or something.."]



def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    gpio.output(24, gpio.LOW)
    gpio.output(25, gpio.LOW)
    return s

def setupConnection():
    s.listen(1)     # allows only one connection
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def dataTransfer(conn):
    data = conn.recv(1024)
    data = data.decode('UTF-8')
    command = data
    if command == 'TURN RIGHT':
        reply = 'Turning right'
        ser.write("right")
        print("Turning Right")
    elif command == 'CONNECT':
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
    elif command == 'MOVIE':
        reply = movies[randint(0,5)]
    elif command == 'KILL':
        gpio.output(24, gpio.LOW)
        gpio.output(25, gpio.LOW)
        print("Shutting down")
        reply = "Disconnected"
        conn.sendall(str.encode(reply))
        gpio.cleanup()
        s.close()
    else:
        reply = 'Unknown Commnad'
        print(reply)
        
    conn.sendall(str.encode(reply))
    print("Data has been sent!")


s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        gpio.cleanup()
        break
    
    

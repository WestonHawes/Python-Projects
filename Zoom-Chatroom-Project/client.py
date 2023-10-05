import socket
import threading
import time


nickname = input("Choose your nickname: ")
priv = "student"

#name of instructor to connect to
iname = input("what instructor are you joining: ")

#Connecting to main server <use main server ip>
SERVER = '10.62.77.151'
SERVER = socket.gethostname()
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((SERVER, 8080))
instructor = None

#listening to serving and sending nickname
def receive():
    while True:
        try:
            message = instructor.recv(1024).decode()
            print(message)
        except:
            print("An error occured! rec")
            instructor.close()
            break
def iReceive():
    i=0
    while True:
        try:
            #sleep to make sure socket buffer doesn't flood
            time.sleep(.5)
            message = client.recv(1024).decode()

            #send privilege
            if message == 'PRIV' :
                client.send(priv.encode())
            #send nickname
            elif message == 'NICK':
                client.send(nickname.encode())
            #send name of instructor to connect to
            elif message == 'INAME':
                client.send(iname.encode())
            #receive instructor IP
            elif message == 'INSTR':
                client.send('READY'.encode())
                instrIp = client.recv(1024).decode()
                break
            
            #wait for instructor if instructor hasn't connected yet
            else:
                time.sleep(.5)
                client.send("OK".encode())
                print("waiting for Instructor")
        except:
            print("An error occured! irec")
            client.close()
            break
    connectInstructor(instrIp)

#connecting to server
def connectInstructor(instrIp) :
    try:
        #close connection to main server
        client.close()
        print(instrIp)
        global instructor

        #initilize instructor socket object
        instructor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #connect student to instructor
        instructor.connect((instrIp, 8082))
        instructor.send(nickname.encode())

        #start write and receive threads
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
        write_thread = threading.Thread(target=write)
        write_thread.start()
    except:
        print('error: not connected to instructor')
        instructor.close()

def write():
    while True:
        try:
            m = input('').split(' ', 1)

            if m[0] == '-h':
                print("help command")
                print("-pm <recipient name> <message>: send private message")
            else:

                message = '{}: {}'.format(nickname,' '.join(m))
                #message = '{}: {}'.format(nickname,input(''))
                instructor.send(message.encode())
        except:
            print("An error occured! w")


#starting threads for listening and writing
#receive_thread = threading.Thread(target=iReceive)
#receive_thread.start()

iReceive()
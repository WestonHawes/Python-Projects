import socket
import threading
import time
#create a socket object
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostbyname(socket.gethostname()))
SERVER = '10.62.78.99' #socket.gethostbyname(socket.gethostname())
#use main server ip
SERVER = socket.gethostname()
#bind server to an ip with a port
#print(SERVER)
serv.bind((SERVER,8080))
serv.listen()
clients = []
nicknames = []
instructorNames = []
studentDict = {}
instructorDict ={}
#print(instructorDict)
#broadcast 
def broadcast(message):
    for client in clients:
        client.send(message)

#multicast should be used for private messages to individuals or groups

#handler
def handleStudent(client, instr): # not indexing correctly
    while True:
        try:
            #broadcasting messages
            #client is addressing all clients
            if instr in instructorDict:
                while True:
                    client.send('INSTR'.encode())
                    msg = client.recv(1024).decode()
                    if msg == 'READY':
                        client.send(instructorDict[instr].encode())
                        index = clients.index(client)
                        #clients.remove(client)
                        client.close()
                        nickname = nicknames[index]
                        print("successfully connected " + nickname + " to " + instr)
                        break
                break
            else:
                time.sleep(1)
                client.send('WAIT'.encode())
                msg = client.recv(1024).decode()
        except:
            #removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode())
            studentDict.pop(nickname, None)
            break

#receive function
def receive():
    while True:
        client, address = serv.accept()
        print("connected with {}".format(str(address)))
        
        client.send('PRIV'.encode())
        priv = client.recv(1024).decode()
        if priv == 'student' :
            #Request and STore nickname
            client.send('NICK'.encode())
            nickname = client.recv(1024).decode()
            nicknames.append(nickname)
            studentDict[nickname] = address
            clients.append(client)
            client.send('INAME'.encode())
            instr = client.recv(1024).decode()
            thread = threading.Thread(target=handleStudent, args = (client, instr,))
            thread.start()
        elif priv == 'instructor':
            client.send('INAME'.encode())
            instructorName = client.recv(1024).decode()
            instructorNames.append(instructorName)

            instructorDict[instructorName] = address[0]
            print(instructorDict)
            print(instructorName)
            client.close()
        #Print and broadcast nickname
        #print("Nickname is {}".format(nickname))
        #broadcast("{} joined!".format(nickname).encode())
        #client.send('Connected to server!'.encode())
        
        #start handling thread for client
        #thread = threading.Thread(target=handle, args = (client,))
        #thread.start()

thread = threading.Thread(target = receive())
thread.start()
import socket
import threading
import time
#create a socket object
iname = input("what is your name: ")
SERVER = '10.62.78.99' #socket.gethostbyname(socket.gethostname())
#use main server Ip
SERVER = socket.gethostname()

ISERVER = '' #socket.gethostbyname(socket.gethostname())
ISERVER = socket.gethostname()
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((SERVER, 8080))
priv = "instructor"

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((ISERVER, 8082))
serv.listen()
clients = []
nicknames = []
rooms = [[]]
studentDict = {}
#broadcast 

#multicast should be used for private messages to individuals or groups
def iReceive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'PRIV' :
                client.send(priv.encode())
            elif message == 'INAME':
                client.send(iname.encode())
                break
        except:
            print("An error occured!")
            client.close()
            break
    try:
        inst_write_thread = threading.Thread(target = inst_write)
        inst_write_thread.start()
        rooms[0].append(iname)
        receive()
    except:
        print("client wasn't recieved")

#handler
def handle(nickname, client):
    while True:
        try:
            #broadcasting messages
            #client is addressing all clients
            message = client.recv(1024)

            checkMessage = message.decode().split(' ', 3)

            if checkMessage[1] == '-pm':
                #           (sender, message)
                privateMessage(nickname, checkMessage[2], checkMessage[3])
            else:
            #print message from student
            #print(message.decode())
                broadcastRoom(nickname, getRoom(nickname), message)
        except:
            #removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode())
            nicknames.remove(nickname)
            clientRoom = getRoom(nickname)

            rooms[clientRoom].pop(nickname)
            studentDict.pop(nickname)
            break

def privateMessage(sender, recipient, message):
    if recipient == iname:
        print('{}: {}'.format("pm from "+sender, message))
    elif recipient in studentDict:
        studentDict[recipient].send('{}: {}'.format("pm from "+sender, message).encode())
    else:
        studentDict[sender].send("error sending pm".encode())

def getRoom(nickname):
    for r, i in enumerate(rooms):
        if nickname in i:
            return r

#broadcast only to room ur in
def broadcastRoom(nickname, room, message):
    for person in rooms[room]:
        if person in studentDict and person != nickname:
            studentDict[person].send(message)
        elif person == iname:
            print(message.decode())

def broadcast(message):
    for client in clients:
        client.send(message)

#receive function
def receive():
    while True:
        (client, address) = serv.accept()
        print("connected with {}".format(str(address)))
        
        #Request and STore nickname
        #client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)
        studentDict[nickname] = client
        #Print and broadcast nickname
        print("{} joined".format(nickname))
        broadcast("{} joined! ".format(nickname).encode())
        client.send(('Connected to '+ iname +'!').encode())
        #breakout room tests
        #rooms.append([])
        #rooms.append([])
        #rooms.append([])
        #if nickname[0] == 'A':
        #    rooms[1].append(nickname)
        #elif nickname[0] == 'B':
        #    rooms[2].append(nickname)
        #elif nickname[0] == 'C': 
        #    rooms[3].append(nickname)
        #else:
        rooms[0].append(nickname)
        print(rooms)
        #print(getRoom(nickname))
        #print(studentDict)
        #start handling thread for client
        thread = threading.Thread(target=handle, args = (nickname, client,))
        thread.start()

#def pclients():
#    while True:
#        print(clients)
#        time.sleep(2)

# def inst_write():
#     while True:
#         try:
#             message = '{}: {}'.format(iname,input(''))
#             print(message)
#             broadcast(message.encode())
#         except:
#             print("An error occured! inst_broad")
#             #break
def addToRoom(nickname, index):
    if (nickname in studentDict or nickname == iname) and index < len(rooms):
        curr = getRoom(nickname)
        rooms[curr].remove(nickname)
        rooms[index].append(nickname)
        broadcast((nickname + " added to breakout room #" + str(index)).encode())
    else:
        print("person or room is not in this session!")

# delete room; add students to main
def deleteRoom(index):
    rem_room = rooms.pop(index)
    
    for student in rem_room:
        rooms[0].append(student)

# delete all rooms; add students to main
def deleteAllRooms():
    i = len(rooms)-1

    while i > 0:
        deleteRoom(i)
        i = i - 1

def inst_write():
    while True:
        #command parser
        try:
            m = input('').split(' ', 1)
            
            if m[0] == '-h':
                print("help command")
                print("-pn: print names of students")
                print("-pr: print all rooms")
                print("-cbr <# of br rooms> : create empty rooms")
                print("-atb <name of person> <index # of room>: add to breakout room")
                print("-br_all <message>: broadcast to all")
                print('-dr <index # of room>: delete room; adds clients to main')
                print('-dar: delete all rooms; add students to main')
                print("-pm <recipient name> <message>: send private message")

            #pn: print names of students
            elif m[0] == '-pn':
                print(nicknames)
            
            #pr: print all rooms
            elif m[0] == '-pr':
                print(rooms)
            
            #-cbr <# of br rooms> : create empty rooms
            elif m[0] == '-cbr':
                numOfRooms = int(m[1])
                i = 0
                while i < numOfRooms:
                    rooms.append([])
                    i = i + 1  
                print(rooms)

            #-atb <name of person> <index of room>: add to breakout room
            elif m[0] == '-atb':
                i = m[1].split(' ', 1)
                addToRoom(i[0], int(i[1]))
                print(rooms)

            elif m[0] == '-br_all':
                broadcast(('{}: {}'.format(iname,m[1])).encode())

            elif m[0] == '-dr':
                deleteRoom(int(m[1]))
                print(rooms)
            
            elif m[0] == '-dar':
                deleteAllRooms()
                print(rooms)

            elif m[0] == '-pm':
                i = m[1].split(' ', 1)
                privateMessage(iname ,i[0], i[1])

            else:
                message = '{}: {}'.format(iname,' '.join(m))
                #print(message)
                broadcastRoom(iname,getRoom(iname),message.encode())
            
        except:
            print("An error occured! inst_write")
            #break


receive_thread = threading.Thread(target = iReceive())
receive_thread.start()
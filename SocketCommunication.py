#from socket import *

#serverSocket = socket(AF_INET,SOCK_STREAM)
#serverSocket.bind(('127.0.0.1',58727))
#serverSocket.listen(5)
#connectionSock,addr=serverSocket.accept()

#print(str(addr),"Connected")

#while True:
#    data = connectionSock.recv(8192)
#    print("Received :",data.decode('utf-8'))

#    connectionSock.send(data)

#    if(data.decode('utf-8')=='-1'):
#        print('Disconnected')
#        break 

import socket
 
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5050))
s.listen(5)
#try:
#    print ("is waiting")

#    client, address = s.accept()
#    print(s.getsockname())

#    print(str(address),"Connected")

    
#    while 1:
#        a=0
#        for i in range(100):
#            a+=1
#        d = client.recv(size)
#        if d:
#            print (list(map(float,d.decode()[:len(d)-1].split(','))))
#        client.send("recieved".encode())
       
 
#except:
#    print("closing socket")
#    client.close()
#    s.close()

print ("is waiting")

client, address = s.accept()
print(s.getsockname())

print(str(address),"Connected")
while 1:
    d = client.recv(size)
    if d:
        print(d.decode().split(','))
        #try:
        #    IMU=list(map(float,d.decode()[:len(d)-2].split(',')))
        #except:
        #    client.recv(size)
        #    continue
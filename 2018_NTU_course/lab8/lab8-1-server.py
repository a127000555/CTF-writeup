from socket import *
serverPort = 12002
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('0.0.0.0' , serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
while True:

	clientSocket, clientAddress = serverSocket.accept()  
	message = clientSocket.recv(512)  
	print("From:" , clientAddress , ", msg:" , message.decode())
	# modifiedMessage = message.decode().upper()
	# clientSocket.send(modifiedMessage.encode())  
	clientSocket.close()
	
import socket
import threading
from block import Block

class ClientThread(threading.Thread) :
    def __init__(self,ip,port,clientsocket,blockchain):
        threading.Thread.__init__(self)
        self.socket = socket.socket()
        self.ip = ip
        self.port = port
        self.blockchain = blockchain
        self.clientsocket = clientsocket

    def run(self):
        print(f"On envoie le block {self.blockchain.chain[-1].block_hash} , au client  {self.clientsocket}")

        block = self.blockchain.chain[-1]
        newblock=Block(None,self.blockchain.chain[-1],"bonjour")
        trame=f"{newblock.block_hash}"
        self.clientsocket.send(trame.encode())#Trame de block
        #attente de réception.

        trame = self.clientsocket.recv(2048).decode()
        trame_client = trame.split(";")
        newblock.block_hash=trame_client[0]
        newblock.sign=trame_client[1]

        #vérfication pas complète, le miineur peut renvoyer n'importe quel hash commençant par 0
        if newblock.block_hash[0] == '0' and int(self.blockchain.chain[-1].block_hash,16) == int(block.block_hash,16): 
            self.blockchain.chain.append(newblock)
            self.clientsocket.send("good".encode())
            print(f"Block ajouté : {self.blockchain.chain[-1].block_hash}")
            for x in range(len(self.blockchain.chain)):
                print(f"Blockchain : {self.blockchain.chain[x].block_hash}")
        else:
            self.clientsocket.send("bad".encode())
            print(f"Block déjà ajouté")

        # self.node_socket.close()

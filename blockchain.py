#!/usr/bin/env python3

### DISTIBUEE !


import socket
import os
from block import Block
from clientthread import ClientThread

class Blockchain:
    def __init__(self, socket, host, port):
        self.chain = [Block.genesis_block()]
        self.blockchain_socket = socket
        self.host=host
        self.port=port
        self.blockchain_socket.bind((self.host, self.port))

    def start_blockchain(self, host, port):
        while True :
            print("On attend un client")
            self.blockchain_socket.listen()
            (client, (ip,port)) = self.blockchain_socket.accept()
        
            newthread = ClientThread(ip, port,client,self)
            newthread.start()

def main():
    print("Creation blockchain")
    Blockchain(socket.socket(socket.AF_INET, socket.SOCK_STREAM),'',15555).start_blockchain("127.0.0.1", 15555)
        
if __name__ == "__main__" :
    main()
    
        
# #création liste avec le premier bloc (genesis bloc <=> bloc d'origine)

# block_chain = [Block.create_genesis_block()]

# print("le bloc genesis a été créé !")
# print("Hash:%s" % block_chain)

# #création de 10 blocs, chaque nouveau bloc est ajouté au dernier

# num_blocks_to_add = 10

# for i in range(1,num_blocks_to_add+1):
#         block_chain.append(Block(block_chain[-1].hash,
#                                             "DATA!",
#                                             datetime.datetime.now()))

#         print("Block #%d a été créé")
#         print("Block #%d hash: %s" % (i, block_chain[i].hash))
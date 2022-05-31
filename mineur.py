#!/usr/bin/env python3
from block import *
from blockchain import Blockchain
import hashlib
import socket
import os

###COPIE DE LA BLOCKCHAIN

#évalutation de performance, temps d'exe, nb itération

#+diagramme réseau, 

# blockchain et mineur -> noeuds.

class Mineur:
    def __init__(self, id, socket, host, port):
        self.mineur_socket = socket
        self.host=host
        self.port=port
        self.id = id
        self.value=0

    def proof_of_work(self):

        #ajouter un nonce qui varie çà chaque itération, à renvoyer également.
        block=(self.mineur_socket.recv(2048)).decode()
        
        proof = 0
        flag=False
        while flag is False : 
            hash_operation = hashlib.sha256( 
                str(proof**2 - int(block,16)**2).encode()).hexdigest()
            if hash_operation[0] == '0': 
                flag = True
            else:
                proof += 1
        print(proof)
        return (hash_operation, proof)
    

    def give_hash(self):
        #self.mineur_socket.connect((self.host, self.port))
        
        (hash,proof)=self.proof_of_work()
        trame=f"{hash};{self.id}"
        print(trame)
        self.mineur_socket.send(trame.encode())
        trame=self.mineur_socket.recv(2048).decode()
        if trame == "good" :
            self.value+=proof
        elif trame == "bad"  :
            self.value+=(proof/2)
        
        #self.mineur_socket.close()
        
    def start(self) :
        self.mineur_socket.connect((self.host, self.port))
        while True :
            print("démarrage du minage...")
            self.give_hash()
            print("fin de minage")
        self.mineur_socket.close()

        
def main():
    print("Creation mineur")
    Mineur(1, socket.socket(socket.AF_INET, socket.SOCK_STREAM),"127.0.0.1", 15555).start()
        
if __name__ == "__main__" :
    main()

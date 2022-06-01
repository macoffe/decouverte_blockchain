#!/usr/bin/env python3

import sys
from time import sleep
import socket
import hashlib
import json
from flask import Flask, request
import requests

from block import Block
from blockchain import Blockchain

###COPIE DE LA BLOCKCHAIN
#évalutation de performance, temps d'exe, nb itération
#+diagramme réseau, 
# blockchain et mineur -> noeuds.

app =  Flask(__name__)

class Node:
    def __init__(self, id, init_blockchain = False):#, node_approuveur = False):
        self.id = id
        self.value=0
        if init_blockchain is True:
            self.blockchain = Blockchain(init_bc=True)
            self.blockchain.to_string()
        else:
            self.blockchain = Blockchain()
            result = requests.get('http://127.0.0.1:5000/get_blockchain')
            json_blockchain = result.json()
            for block in json_blockchain["chain"]:
                new_block = Block(block[0], block[1], block[2], block[3])
                self.blockchain.chain.append(new_block)
            self.blockchain.to_string()

    @app.route('/get_blockchain', methods=['GET'])
    def get_blockchain():
        chain_data = []
        for block in node.blockchain.chain:
            block_data = []
            block_data.append(block.sign)
            block_data.append(block.previous_hash)
            block_data.append(block.hash)
            block_data.append(block.is_mined)
            chain_data.append(block_data)
        return json.dumps({"chain": chain_data})

    @app.route('/post_newblock', methods=['POST'])
    def post_newblock():
        hash_operation = request.args.get('hash_operation')
        node_id = request.args.get('node_id')
        last_hash = request.args.get('last_hash')

        print("test post nb")

        new_block = Block(node_id, last_hash, hash_operation, is_mined=True)
        node.blockchain.chain.append(new_block)

        node.blockchain.to_string()
        return "newblock posted"
        
    
    # def send_transaction(self):
    #     #self.node_socket.bind((self.host, self.port))
    #     while True :
    #         try:
    #             self.node_socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             self.node_socket.bind((self.host, self.port))
    #             print("On attend un client")
    #             self.node_socket.listen(3)
    #             (client, (ip,port)) = self.node_socket.accept()
            
    #             newthread = ClientThread(ip, port,client,self)
    #             newthread.start()

    #             self.node_socket.close()
    #         except:
    #             print("pas possible d'envoyer un bloc pour le moment")
    #             sleep(5)

    # def proof_of_work(self):

    #     #ajouter un nonce qui varie çà chaque itération, à renvoyer également.
    #     block=(self.node_socket.recv(2048)).decode()
        
    #     proof = 0
    #     flag=False
    #     while flag is False : 
    #         hash_operation = hashlib.sha256( 
    #             str(proof**2 - int(block,16)**2).encode()).hexdigest()
    #         if hash_operation[0] == '0': 
    #             flag = True
    #         else:
    #             proof += 1
    #     print(proof)
    #     return (hash_operation, proof)

    def proof_of_work(self, data, last_block_hash):
        nonce = 0
        hash_operation = "1"

        while hash_operation[0] != '0':
            if last_block_hash == node.blockchain.chain[-1].previous_hash:
                return (None, None)
            nonce += 1
            work = f"{nonce}{data}{self.blockchain.chain[-1].hash}"
            hash_operation = hashlib.sha256(work.encode()).hexdigest()
            print(f"{work} > {hash_operation}")
        print(nonce)

        return (hash_operation, nonce)

    @app.route('/check_work', methods=['POST'])
    def check_work():
        hash_operation = request.args.get('hash_operation')
        nonce = request.args.get('nonce')
        data = request.args.get('data')
        last_hash = request.args.get('last_hash')

        check = f"{nonce}{data}{last_hash}"
        hash_check = hashlib.sha256(check.encode()).hexdigest()

        if hash_check == hash_operation:
            new_block = Block(node.id, last_hash, hash_operation, is_mined=True)
            node.blockchain.chain.append(new_block)
            #for ip in ip_list
            requests.post(f'http://127.0.0.1:5004/post_newblock?hash_operation={hash_operation}&node_id={node.id}&last_hash={last_hash}')
            requests.post(f'http://127.0.0.1:5001/post_newblock?hash_operation={hash_operation}&node_id={node.id}&last_hash={last_hash}')
            requests.post(f'http://127.0.0.1:5002/post_newblock?hash_operation={hash_operation}&node_id={node.id}&last_hash={last_hash}')
            return "true"
        else:
            print("false")
            return "false"

    @app.route('/post_transaction', methods=['POST'])
    def post_transaction():
        data = request.args.get('data')
        last_block_hash = node.blockchain.chain[-1].hash
        #last_block_previous_hash = node.blockchain.chain[-1].previous_hash
        hash_operation, nonce = node.proof_of_work(data, last_block_hash)
        if hash_operation != None:
            #for ip in ip_list
            print("test")
            response = requests.post(f'http://127.0.0.1:5002/check_work?hash_operation={hash_operation}&nonce={nonce}&data={data}&last_hash={last_block_hash}')

        # block = Block(node.id, node.blockchain.chain[-1].previous_hash, hash_operation)
        return data

        
    # def get_transaction():

    # def give_hash(self):
        #self.node_socket.connect((self.host, self.port))
        
        # (hash,proof)=self.proof_of_work()
        # trame=f"{hash};{self.id}"
        # print(trame)
        # self.node_socket.send(trame.encode())
        # trame=self.node_socket.recv(2048).decode()
        # if trame == "good" :
        #     self.value+=proof
        # elif trame == "bad" :
        #     self.value+=(proof/2)
        
        #self.node_socket.close()
        
    # def start(self) :
        #self.node_socket.connect((self.host, self.port))
        # while True :
        #     try:
        #         self.node_socket.connect((self.host, self.port))
        #         print("tentative de minage...")
        #         self.give_hash()
        #         print("fin de minage")
        #         self.node_socket.close()
        #     except:
        #         print("pas de transaction disponible")
        #         sleep(5)
                
        #self.node_socket.close()

        
# def main():
#     print("Creation mineur")
#     Node(2, socket.socket(socket.AF_INET, socket.SOCK_STREAM),"127.0.0.1", 15555, init_blockchain=False).start()

# def main():
#     if sys.argv[1] == 1 :
#         print("Creation blockchain")
#         Node(sys.argv[2],socket.socket(socket.AF_INET, socket.SOCK_STREAM),"127.0.0.1", 15555, init_blockchain=True).start_blockchain()
#     elif sys.argv[1] == 0 :
#         print("Creation node")
#         Node(sys.argv[2],socket.socket(socket.AF_INET, socket.SOCK_STREAM),"127.0.0.1", 15555).start_blockchain()
#     else :
#         print("Confirme node")
#         Node(sys.argv[2],socket.socket(socket.AF_INET, socket.SOCK_STREAM),"127.0.0.1", 15555, node_approuveur=True).start_app()

if __name__ == "__main__" :
    if sys.argv[2] == "init" :
        print("Creation blockchain")
        node = Node(sys.argv[1], init_blockchain=True)
    elif sys.argv[2] == "approuver" :
        node = Node(sys.argv[1])
    else:
        node = Node(sys.argv[1])
        response = requests.post(f'http://127.0.0.1:5000/post_transaction?data={sys.argv[2]}')
        # print(response.text)

    app.run(debug=True, port=sys.argv[3])

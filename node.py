#!/usr/bin/env python3

from ast import arg
import random
import sys
import threading
import hashlib
import json

from flask import Flask, request
import requests

from block import Block
from blockchain import Blockchain

#évalutation de performance, temps d'exe, nb itération

app =  Flask(__name__)

class Node:
    def __init__(self, id, init_blockchain = False):
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

        new_block = Block(node_id, last_hash, hash_operation, is_mined=True)
        node.blockchain.chain.append(new_block)

        node.blockchain.to_string()
        return "newblock posted"

    def proof_of_work(self, data, last_block_hash):
        nonce = random.randint(0, 1000)
        hash_operation = "1"

        while hash_operation[:2] != '00':
            if last_block_hash == node.blockchain.chain[-1].previous_hash:
                return (None, None)
            nonce = random.randint(0, 1000)
            print(node.blockchain.chain[-1].hash)
            work = f"{nonce}{data}{node.blockchain.chain[-1].hash}"
            hash_operation = hashlib.sha256(work.encode()).hexdigest()
            print(f"{work} > {hash_operation}")

        return (hash_operation, nonce)

    @app.route('/check_work', methods=['POST'])
    def check_work():
        hash_operation = request.args.get('hash_operation')
        nonce = request.args.get('nonce')
        data = request.args.get('data')
        last_hash = request.args.get('last_hash')

        check = f"{nonce}{data}{last_hash}"
        hash_check = hashlib.sha256(check.encode()).hexdigest()

        if hash_check == hash_operation and last_hash == node.blockchain.chain[-1].hash:
            new_block = Block(node.id, last_hash, hash_operation, is_mined=True)
            node.blockchain.chain.append(new_block)
            node.blockchain.to_string()
            #for ip in ip_list
            threading.Thread(target=send_newblock, args=("5000", hash_operation, node.id, last_hash)).start()
            threading.Thread(target=send_newblock, args=("5002", hash_operation, node.id, last_hash)).start()
            threading.Thread(target=send_newblock, args=("5003", hash_operation, node.id, last_hash)).start()
            return "true"   
        else:
            return "false"

    @app.route('/post_transaction', methods=['POST'])
    def post_transaction():
        data = request.args.get('data')
        last_block_hash = node.blockchain.chain[-1].hash
        hash_operation, nonce = node.proof_of_work(data, last_block_hash)
        if hash_operation != None:
            #for ip in ip_list, select one
            threading.Thread(target=send_check, args=("5001", hash_operation,nonce,data,last_block_hash)).start()

        return data

def send_transaction(port, data):
    requests.post(f'http://127.0.0.1:{port}/post_transaction?data={data}')
def send_check(port, hash_operation, nonce, data, last_block_hash):
    requests.post(f'http://127.0.0.1:{port}/check_work?hash_operation={hash_operation}&nonce={nonce}&data={data}&last_hash={last_block_hash}')
def send_newblock(port, hash_operation, node_id, last_hash):
    requests.post(f'http://127.0.0.1:{port}/post_newblock?hash_operation={hash_operation}&node_id={node_id}&last_hash={last_hash}')

if __name__ == "__main__" :
    if sys.argv[2] == "init" :
        print("Creation blockchain")
        node = Node(sys.argv[1], init_blockchain=True)
    elif sys.argv[2] == "approuver" :
        node = Node(sys.argv[1])
    else:
        node = Node(sys.argv[1])
        #for ip in ip_list
        threading.Thread(target=send_transaction, args=("5000", sys.argv[2])).start()
        threading.Thread(target=send_transaction, args=("5002", sys.argv[2])).start()
        threading.Thread(target=send_transaction, args=("5003", sys.argv[2])).start()

    app.run(port=sys.argv[3])

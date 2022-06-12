#!/usr/bin/env python3

from block import Block
import hashlib

class Blockchain: 
    def __init__(self, init_bc=False):
        #self.unconfirmed_transactions = []
        self.chain = []
        self.nodes_ips = []
        if init_bc is True:
            self.genesis_block()
 
    def genesis_block(self):
        b_hash = hashlib.sha256("genesis".encode()).hexdigest()
        genesis_block = Block("root", "0",b_hash, is_mined=True)
        self.chain.append(genesis_block)
        # b_hash = hashlib.sha256("genesis2".encode()).hexdigest()
        # genesis_block = Block("root", "0",b_hash, is_mined=True)
        # self.chain.append(genesis_block)

    # def last_block(self):
    #     return self.chain[-1]

    def to_string(self):
        print("blockchain---------------------------------------------------")
        for block in self.chain:
            print(block.hash)
        print("ip-----------------------------------------------------------")
        for ip in self.nodes_ips:
            print(ip)
        print("-------------------------------------------------------------")
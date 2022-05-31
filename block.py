#!/usr/bin/env python3
import hashlib

class Block:
    
    def __init__(self, sign, previous_block_hash, data):
        self.previous_hash=previous_block_hash
        self.data = f"{data}{previous_block_hash}"
        self.sign = sign
        self.block_hash=hashlib.sha256(self.data.encode()).hexdigest()
        self.is_mined = False

    @staticmethod
    def genesis_block():
        return Block("root", "0","genesis_block")
        
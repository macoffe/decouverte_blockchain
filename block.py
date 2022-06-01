#!/usr/bin/env python3
import hashlib
import json

class Block:
    
    def __init__(self, sign, previous_block_hash, block_hash, is_mined = False):
        self.hash = block_hash
        self.previous_hash = previous_block_hash
        #self.data = f"{data}{previous_block_hash}"
        #self.data = data
        self.sign = sign
        # self.block_hash=hashlib.sha256(self.data.encode()).hexdigest()
        self.is_mined = is_mined

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        
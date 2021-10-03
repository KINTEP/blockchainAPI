from hashlib import sha256
from urllib.parse import urlparse
import json
import time
import pickle
import jsonpickle
from flask import Flask, request
import requests
import datetime
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import os
from Crypto.PublicKey import RSA
from blockchainv1.adresses import Addresses
from blockchainv1.models import BlocksDB
from blockchainv1.helpers import save_block

class Mempool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, tx):
        self.transactions.append(tx)
        return True

class UTXOset:
    pass

class TxIn:
    """docstring for TxIn"""
    def __init__(self, inputs_id):
        self.inputs_id = inputs_id
        self.block_idx = None

    def tx(self):
        return  get_tx(self.block_idx, self.inputs_id)

    def is_transaction_in_chain(self):
        tx1 = get_tx(self.block_idx, self.inputs_id)
        if tx1:
            return True
        else:
            return False

    def is_amount_yours(self):
        """
        message = self.tx.message()
        message['tx_id'] = self.tx.tx_id
        message = str(message)
        hash2 = SHA256.new(message.encode())
        sig = self.tx.signature
        try:
            pkcs1_15.new(RSA.import_key(self.tx.pub_key)).verify(hash2, sig)
            return True
        except:
            return False
            """
        """This function takes the signature and checks if it was signed by the public key"""
        return self.tx.verify_input()

    def is_passed(self):
        return self.tx.tx_passed()

    def get_value(self):
        return self.tx.tx_out.amount

    def get_pubkey(self):
        return self.tx.tx_out.pub_key


class TxOut:
    def __init__(self, amount, pub_key):
        self.amount = amount
        self.pub_key = pub_key
        self.priv_key = None

    def __repr__(self):
        string = self.__dict__
        return str(string)

    def check_amt(self):
        if self.amount > 0:
            return True
        else:
            return False

class Transaction:
    def __init__(self, tx_in, tx_out, tx_indx):
        self.tx_in = tx_in
        self.tx_out = tx_out
        self.tx_indx = tx_indx
        self.pub_key = None
        self.signature = None
        self.tx_id = self.compute_hash()
        self.block_idx = None

        
    def __repr__(self):
        string = self.__dict__
        return str(string)

    def message(self):
        dict1 = {
            'tx_in':self.tx_in,
            'tx_out':self.tx_out,
            'tx_indx':self.tx_indx,
            'pub_key':self.pub_key
        }
        return dict1

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        data = self.message()
        
        block_string = str(data)
        
        return sha256(block_string.encode()).hexdigest()

    def sign_trans(self, priv_key):
        message = self.message()
        #message['tx_id'] = self.tx_id
        message = str(message)
        hash2 = SHA256.new(message.encode())
        signature1 = pkcs1_15.new(RSA.import_key(priv_key))
        sig = signature1.sign(hash2)
        self.signature = sig
        return True

    def verify_input(self):
        """Verifies if the input tx has a valid signature!"""
        message = self.message()
        #message['tx_id'] = self.tx_id
        message = str(message)
        hash2 = SHA256.new(message.encode())
        sig = self.signature
        try:
            pkcs1_15.new(RSA.import_key(self.pub_key)).verify(hash2, sig)
            return True
        except:
            return False

    def check_amount(self):
        """This functions returns true if the input amt is greater or equal to the output amt"""
        output_amt = self.tx_out.amount
        input_amt = 0
        for tx_in in self.tx_in:
            input_amt += tx_in.tx_out.amount
        return input_amt >= output_amt

    def tx_passed(self):
        if not self.tx_out.check_amount():
            return False
        if not check_amount():
            return False
        if not verify_input():
            return False
        return True

    def update_balances(self):
        sender = self.pub_key
        receiver = self.tx_out.pub_key
        amount = self.tx_out.amount
        sender.sub_amount(amount)
        receiver.add_amount(amount)
        return True


    def fee(self):
        pass

class Block:
    def __init__(self):
        self.index = 0
        self.transactions = []
        self.timestamp = datetime.datetime.utcnow
        self.previous_hash = None
        self.nonce = 0
        self.difficulty = 2
        self.hash_value = ''

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        data = {
            'index':self.index,
            'trans': self.transactions,
            'time': self.timestamp,
            'prev_hash': self.previous_hash,
            'nonce': self.nonce,
            'diffi': self.difficulty
        }
        
        block_string = str(data)
        
        return sha256(block_string.encode()).hexdigest()

    def view_data(self):
        return self.__dict__
    
    def proof_of_work(self):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        self.nonce = 0

        computed_hash = self.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            self.nonce += 1
            computed_hash = self.compute_hash()
            
        self.hash_value = computed_hash
        
        return True

    def add_new_transaction(self, trans1):
        #check transacrion b4 added to block! TODO
        #trans = str(trans1)
        #trans_hash = sha256(trans.encode()).hexdigest()
        self.transactions.append(trans1)
        
    def is_valid_proof(self):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (self.hash_value.startswith('0' * self.difficulty) and
                self.hash_value == self.hash_value)

    def reset_tx_block_idx(self):
        for tx in self.transactions:
            tx.block_idx = self.index
        return True



class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2
    name = ""
    
    def __init__(self):
        self.chain = BlocksDB.query.all()
        self.nodes = set()

    def add_nodes(self, ip_addr):
        parsedUrl = urlparse(ip_addr)
        self.nodes.add(parsedUrl.netloc)

    def main_chain(self):
        return jsonpickle.encode({'chain': self.chain, 'length':len(self.chain)}, unpicklable=False)

    @property
    def last_block(self):
        if len(self.chain) < 1:
            return None
        q1 = self.chain[-1]
        l_block = q1.blocks
        return jsonpickle.decode(l_block)


    def add_block(self, block):
        #Inspect transactions in the block!
        last_blck = self.last_block
        if last_blck is None:
            idx = 0
            block.index = idx
            block.previous_hash = '000000000000000000000000000'
            self.chain.append(block)
            save_block(id = idx, block1 = block)
            return 'Genesis!'

        if not block.is_valid_proof():
            return False

        idx = last_blck.index + 1
        block.index = idx
        block.previous_hash = last_blck.previous_hash
        block.reset_tx_block_idx()
        for tx in block.transactions:
            tx.update_balances()
        self.chain.append(block)
        save_block(id = idx, block1 = block)
        return True

    def is_chain_valid(self):
        for i in range(len(self.chain)-1):
            first_block = self.chain[i]
            second_block = self.chain[i+1]
            if first_block.hash_value != second_block.previous_hash:
                return False
            if not first_block.proof_of_work() and not second_block.proof_of_work():
                return False
        return True

    def consensus(self):
        node_address = self.nodes
        my_lenth = len(self.chain)
        for url in node_address:
            response = requests.get(url+'chain')
            #print(response.status_code)
            if response.status_code == 200:
                chain = response.json()['chain']
                length = response.json()['length']

                if my_lenth < length:
                    self.chain = chain
                else:
                    chain = self.chain
        return True

def compare_chains(chain1, chain2):
    for ch1, ch2 in zip(chain1.chain, chain2.chain):
        hash1 = ch1.compute_hash()
        hash2 = ch2.compute_hash()

        if hash1 != hash2:
            return False
    return True



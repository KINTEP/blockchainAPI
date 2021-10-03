from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from hashlib import sha256
from block import Transaction, TxIn, TxOut, Blockchain, Block
import jsonpickle

from adresses import Addresses

message = 'This is new'

addr = Addresses()
key1 = addr.privateKey()
pub1 = addr.publicKey()

hash1 = sha256(message.encode())
hash2 = SHA256.new(message.encode())
#print(key1)
#print(hash1)

#signature = pkcs1_15.new(key1)#.sign(hash1)
#print(signature.can_sign())
#print(signature)

key = RSA.generate(2048)
pub1 = key.publickey()
#print(key)

signature = pkcs1_15.new(key)#.sign(hash1)
#sig = signature.can_sign()
sig = signature.sign(hash2)
print('*'*30)

def sign_trans(key, msg):
	hash2 = SHA256.new(msg.encode())
	signature = pkcs1_15.new(key)
	sig = signature.sign(hash2)
	return sig

def verify_trans(msg, sig, pubkey):
	hash_msg = SHA256.new(msg.encode())
	try:
		pkcs1_15.new(pubkey).verify(hash_msg, sig)
		return True
	except:
		return False
sig1 = sign_trans(key=key, msg=message)


if verify_trans(message, sig1, pub1):
	print('Valid')
else:
	print('Failed!')

#print(pub1)

#genesis_block

msg = 'Happy Birthday!'
ms = SHA256.new(msg.encode())

f = open('keys/mykey0.pem','r')
key0 = f.read()
key00 = RSA.import_key(key0)
ss1 = sign_trans(key=key00, msg=msg)

f1 = open('keys/mypubkey0.pem','r')
pub0 = f1.read()
pub00 = RSA.import_key(pub0)

#print(verify_trans(msg=msg, sig=ss1, pubkey=pub00))
######################################################

f02 = open('keys/mykey1.pem','r')
key1 = f02.read()
key11 = RSA.import_key(key1)

f2 = open('keys/mypubkey1.pem','r')
pub1 = f2.read()
pub11 = RSA.import_key(pub1)

"""

'Dont send transaction to yourself'

f11 = open('keys/mypubkey2.pem','r')
pub2 = f11.read()
pub22 = RSA.import_key(pub2)

t1_in = TxIn(inputs_id = '00000000000000000')
t1_out = TxOut(amount = 20, pub_key = pub1 )
Tx1 = Transaction(tx_in = [t1_in], tx_out=t1_out, tx_indx=0)
Tx1.pub_key = pub0

#msg = str(Tx1.__dict__)

#ss1 = sign_trans(key=key00, msg=msg)
#print(verify_trans(msg=msg, sig=ss1, pubkey=pub00))
Tx1.sign_trans(priv_key = key0)
sig1 = Tx1.signature
print('Verification of signature')
print(Tx1.verify_input())

blchain = Blockchain()
prev_hash = blchain.last_block.hash_value

block1 = Block(index=1, timestamp='ghagha', previous_hash=prev_hash)
block1.add_new_transaction(Tx1)
block1.proof_of_work()
blchain.add_block(block1)

print(Tx1.verify_input())
from block import get_tx
idx2 = Tx1.tx_id

TN1 = get_tx(idx2)
print('@'*50)
print(TN1.verify_input())
print(Tx1.verify_input())
print('#'*50)



t1_in2 = TxIn(inputs_id = idx2)
#print(t1_in2.tx)
#print(t1_in2.isTransactionInChain())
print(t1_in2.isAmountYours())
t1_out2 = TxOut(amount = 10, pub_key = pub2)
Tx2 = Transaction(tx_in = [t1_in2], tx_out=t1_out2, tx_indx=1)
#Tx2.priv_key = key2
Tx2.pub_key = pub1
"""
import os


def get_chain():
	blocks = os.listdir('database/')
	for bl in blocks:
		print(bl)

get_chain()
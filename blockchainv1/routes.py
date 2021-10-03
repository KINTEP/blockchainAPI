from blockchainv1.adresses import PublicKey
import datetime
import jsonpickle
from blockchainv1.block import Blockchain, Transaction, Block, TxOut, TxIn, Mempool
from blockchainv1 import app, db, api
from blockchainv1.models import BlocksDB
from blockchainv1.helpers import get_tx, get_chain, get_block_of_tx
from flask_restful import Resource, reqparse, abort, fields, marshal_with
import json

mempool = Mempool()
broad_casted_block = []


class GenerateKeys(Resource):
	def get(self):
		addr1 = PublicKey()	
		private = addr1.private_key.decode()
		public = addr1.public_key.decode()
		return {"public key":public, "private key":private}

transaction_put = reqparse.RequestParser()
transaction_put.add_argument("input id", type=str, help = "Input ID required!", required = True)
transaction_put.add_argument("Amount", type=str, help = "Amount required!", required = True)
transaction_put.add_argument("Receiver Adrr", type=str, help = "Receiver Adrr required!", required = True)
transaction_put.add_argument("Sender Adrr", type=str, help = "Sender Adrr required!", required = True)
transaction_put.add_argument("Private Key", type=str, help = "Private Key required!", required = True)

class CreateTransaction(Resource):
	def get(self):
		trans = list(mempool.transactions)
		return {"transactions": jsonpickle.encode(trans)}

	def put(self):
		args = transaction_put.parse_args()

		tx_in = TxIn(inputs_id = args['input id'])
		tx_ut = TxOut(amount = 10, pub_key = args['Receiver Adrr'])
		tx1 = Transaction(tx_in = [tx_in], tx_out=tx_ut, tx_indx = 0)
		tx1.pub_key = args['Sender Adrr']
		tx1.sign_trans(priv_key=args['Private Key'])
		mempool.add_transaction(tx1)
		if mempool:
			return {"Sucess":"Transaction added to mempool!, Wait for confirmation"}
		return {'Failed!':"Please check and try again!"}

class CreateYourBlockChain(Resource):
	"""This is to create your own blockchain!"""
	def get(self):
		pass

	def put(self):
		pass

class AddTransactionToBlock(Resource):
	def get(self):
		pass

	def put(self):
		block = Block()
		args = transaction_put.parse_args()

		tx_in = TxIn(inputs_id = args['input id'])
		tx_ut = TxOut(amount = 10, pub_key = args['Receiver Adrr'])
		tx1 = Transaction(tx_in = [tx_in], tx_out=tx_ut, tx_indx = 0)
		tx1.pub_key = args['Sender Adrr']
		tx1.sign_trans(priv_key=args['Private Key'])
		passed = tx1.tx_passed()
		if passed:
			block.add_transaction(tx1)
			return {"Success":"Transaction successfully added to chain!"}
		return {"Failed":"Something went wrong, please try again"}

class BlockExplorer(Resource):
	def get(self, blck_id):
		res = BlocksDB.query.filter_by(id = blck_id).first()
		return {'block': res.blocks}

class GetChain(Resource):
	def get(self):
		res = BlocksDB.query.all()
		len1 = len(res)
		return {"len":len1, "chain":jsonpickle.encode(res)}

class MineBlock(Resource):
	def get(self):
		pass

	def put(self):
		block = Block()
		args = transaction_put.parse_args()

		tx_in = TxIn(inputs_id = args['input id'])
		tx_ut = TxOut(amount = 10, pub_key = args['Receiver Adrr'])
		tx1 = Transaction(tx_in = [tx_in], tx_out=tx_ut, tx_indx = 0)
		tx1.pub_key = args['Sender Adrr']
		tx1.sign_trans(priv_key=args['Private Key'])
		passed = tx1.tx_passed()
		if not passed:
			return {"Failed":"Transaction wasnt verified successfully"}
		block.add_transaction(tx1)
		proof = block.proof_of_work()
		while not proof:
			print("Block is been mine, this may take some time.........")
		valid = block.is_valid_proof()
		if not valid:
			return {"Failed":"Proof of wasnt verified successfully!"}
		blockchain = Blockchain()
		broad_casted_block.append(block)
		if proof:
			return {"Success":"Block successfully mined and added broadcasted!"}
		return {"Failed":"Something went wrong, please try again!"}

class TxInMempool(Resource):
	def get(self):
		mem = mempool.transactions
		num = len(mem)
		return {"number":num,"transactions": jsonpickle.encode(mem)}

	def put(self):
		pass

class BroadcastData(Resource):
	def get(self):
		broad_cast = broad_casted_block
		if not broad_cast:
			return {"Info":"There are no blocks in the broadcast space"}
		return {"Blocks":broad_cast}

node_address = reqparse.RequestParser()
node_address.add_argument("IP Address", type=str, help = "IP Address required!", required = True)

class BecomeANode(Resource):
	def get(self):
		with open("nodes.db", "r") as file:
			str1 = file.read()
			nodes_list = str1.split("===")
		return {"Nodes":json.dumps(nodes_list[:-1])}
			
	def put(self):
		args = node_address.parse_args()
		addr1 = args['IP Address']
		if addr1:
			with open("nodes.db", "a") as file:
				file.write(f"{addr1}===")
				return {"Success":f"{addr1} has successfully been added"}


class VoteBlock(Resource):
	def get(self):
		pass

	def put(self):
		pass 


api.add_resource(GenerateKeys, '/generatekeys')
api.add_resource(CreateTransaction, '/createtransaction')
api.add_resource(BlockExplorer, '/exploreblocks/<int:blck_id>')
api.add_resource(GetChain, '/getchain')
api.add_resource(TxInMempool, '/txinmempool')
api.add_resource(AddTransactionToBlock, '/addtransactiontoblock')
api.add_resource(MineBlock, '/mineblock')
api.add_resource(BroadcastData, '/broadcastdata')
api.add_resource(BecomeANode, '/becomeanode')







"""
#Step1: Generate private and private keys

#Send all coins to:
gen_priv1 = addr1.private_key()
gen_pub1 = addr1.public_key()

#with open('keys_priv.txt', 'w') as f1:
#	f1.write(str(gen_priv1))

#with open('keys_pub.txt', 'w') as f2:
#	f2.write(str(gen_priv))
"""
"""
#Step2: Create a transaction
tx_in = TxIn(inputs_id = '00000000000000000000000')
tx_ut = TxOut(amount = 1000000, pub_key = gen_pub1)
#print(tx_ut.check_amt())
tx1 = Transaction(tx_in = [tx_in], tx_out=tx_ut, tx_indx = 0)
tx1.pub_key = gen_pub
print(tx1.sign_trans(priv_key=gen_priv))
print(tx1.verify_input())
#print(tx1.compute_hash())
#print(tx1.message())

#Add tx to mempool
#Step 4 Add tx to block
block1 = Block()
block1.index = 0
block1.add_new_transaction(tx1)

print(block1.proof_of_work())
print(block1.is_valid_proof())

#Step 5: Add block to blockchain
blockchain = Blockchain()
print(blockchain.add_block(block1))

#Step6: Save Block to the blockchain

#save_block(block1 = block1)

"""
"""
#Step2: Create a transaction
bidd = 0
txidd = "7733ccdeb508e0495f6de0675f7918998cd426dca1c5ac60244b951ad070853c"
txz1 = get_tx(b_index=bidd, tx_id=txidd)
my_pub_key = gen_pub1#txz1.tx_out.pub_key
my_priv_key = gen_priv1#txz1.tx_out.priv_key

tx_in = TxIn(inputs_id = txidd)
tx_ut = TxOut(amount = 100, pub_key = gen_pub)
tx_ut.priv_key = gen_priv
#print(tx_ut.check_amt())
tx1 = Transaction(tx_in = [tx_in], tx_out=tx_ut, tx_indx = 0)
tx1.pub_key = my_pub_key

print(tx1.sign_trans(priv_key=my_priv_key))
print(tx1.verify_input())
#print(tx1.compute_hash())
#print(tx1.message())

#Add tx to mempool
#Step 4 Add tx to block
blockchain = Blockchain()

block1 = Block()
block1.index = blockchain.last_block.index + 1
block1.add_new_transaction(tx1)

print(block1.proof_of_work())
print(block1.is_valid_proof())

#Step 5: Add block to blockchain

print(blockchain.add_block(block1))




#print(get_block_of_tx(b_index=0))



#g1 = get_chain()
#tx1 = get_tx(b_id=bidd, tx_id=txidd)
#print(tx1)
#print(g1[-1].view_data())

#print(chain1[0].transactions)
#tr1 = get_block_of_tx(b_id=bidd)
#print(get_tx(b_id=bidd, tx_id=txidd))

"""
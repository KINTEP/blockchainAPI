from blockchainv1.models import BlocksDB
import jsonpickle
from blockchainv1 import db

def save_block(id, block1):
	json_block = jsonpickle.encode(block1)
	idx = block1.index
	blockdb = BlocksDB(id = idx, blocks = json_block)
	db.session.add(blockdb)
	db.session.commit()
	return True

def get_chain():
	db11 = BlocksDB()
	q1 = db11.query.all()
	chain = []
	for bl in q1:
		chain.append(jsonpickle.decode(bl.blocks))
	return chain

def get_block_of_tx(b_index):
	chain1 = get_chain()
	txx1 = None
	trans = None
	if not chain1:
		return None
	for block in chain1:
		if block.index == b_index:
			txx1 = block.transactions
	return txx1

def get_tx(b_index, tx_id):
	txxss = get_block_of_tx(b_index=b_index)
	tx1 = None
	if not txxss:
		return None
	for tx in txxss:
		if tx.tx_id == tx_id:
			tx1 = tx
	return tx1
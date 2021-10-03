#Generate addresses for private and public keys as well as sign transactions

from Crypto.PublicKey import RSA
from Crypto.Signature import *
from Crypto.PublicKey import ECC

class Addresses(object):
	"""this clas generate public and private keys"""
	def __init__(self):
		self.key = RSA.generate(2048)

	def private_key(self):
		return self.key.export_key()

	def ecc_keys(self):
		key = ECC.generate(curve='P-256')
		pub = key.pointQ.y
		pri = key.d
		return key, pub

	def public_key(self):
		return self.key.publickey().export_key()

	def balance(self):
		pass


def private_key():
	return RSA.generate(2048).export_key()

class PublicKey:
	def __init__(self, private_key=private_key()):
		self.private_key = private_key
		self.public_key = RSA.import_key(self.private_key).publickey().export_key()
		self.balance = 0

	def add_amount(self, amt):
		self.balance += amt

	def sub_amount(self, amt):
		self.balance -= amt




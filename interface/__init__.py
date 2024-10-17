
import rsa
from hashlib import sha256

from localuser import LocalUser

RSAKeyPair = tuple[rsa.PublicKey, rsa.PrivateKey]

class Interface:

	def __init__(self) -> None:
		
		self.local_user: LocalUser = LocalUser()

	def createUser(self, nickname: str) -> None:
		
		pubkey: rsa.PublicKey
		privkey: rsa.PrivateKey

		pubkey, privkey = rsa.keygen(2048)
		uid = sha256(pubkey + nickname)

		self.local_user.setPrivkey(privkey)
		self.local_user.setPubKey(pubkey)
		self.local_user.setUid(uid)
  
		# TODO add eqqengine acknowledge

	def writePost(self, text: str) -> None:
		pass

	def getUser(self, uid: str) -> None:
		pass

	def getNews(self, uid: str) -> None:
		pass

	def like(self, uid: str) -> None:
		pass

	def follow(self, uid: str) -> None:
		pass

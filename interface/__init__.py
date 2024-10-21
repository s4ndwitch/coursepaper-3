
import rsa
from hashlib import sha256

from interface.localuser import LocalUser
from eqengine import EqEngine

class Interface:
	
	_engine: EqEngine
	_local_user: LocalUser

	def __init__(self) -> None:
		
		self._local_user = LocalUser()
		self._engine = EqEngine()
  
	def shutdown(self) -> None:
		self._engine.shutdown()
  
	def follow(self, uid: str) -> None:
		self._local_user.follow(uid)
  
	def getFollows(self) -> list[str]:
		return self._local_user.getFollows()

	def createUser(self, nickname: str) -> None:
		
		pubkey: rsa.PublicKey
		privkey: rsa.PrivateKey

		pubkey, privkey = rsa.newkeys(2048)
  
		pubkey_str: str = pubkey.save_pkcs1().decode()

		uid = sha256(pubkey_str.encode() + nickname.encode()
               ).hexdigest()

		self._local_user.setUser(
			privkey=privkey,
			pubkey=pubkey,
			uid=uid
		)

		self._engine.handleData(
			[{
				"type": "user",
				"uid": uid,
				"pubkey": pubkey_str,
				"nickname": nickname
			}]
		)

	def writePost(self, text: str) -> None:
		pass

	def getUser(self, uid: str) -> None:
		pass

	def getNews(self, uid: str) -> None:
		pass

if __name__ == "__main__":
	
	pass

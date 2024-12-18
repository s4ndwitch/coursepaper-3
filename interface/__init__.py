
import rsa
from hashlib import sha256

from interface.localuser import LocalUser
from eqengine import EqEngine

class Interface:
	
	_engine: EqEngine
	_local_user: LocalUser

	def __init__(self, address: str, port: int = 8080, nickname: str = "",
              db_file: str = "db.sqlite", peer_file: str = "peer.ini", local_file: str = "localuser.ini") -> None:
		
		self._local_user = LocalUser(config_file=local_file)
  
		uid: str = self._local_user.getUid()
  
		if uid is None:
			if nickname != "":
				pubkey: str
		
				uid, pubkey = self._createUser(nickname=nickname)
		
				self._engine = EqEngine(uid=uid, address=address, port=port,
                            db_file=db_file, peer_file=peer_file)
		
				self._engine.handleData(
					[{
						"type": "user",
						"uid": uid,
						"pubkey": pubkey,
						"nickname": nickname
					}]
				)
			else:
				raise("Cannot create a user")
		else:
			self._engine = EqEngine(uid=uid, address=address, port=port,
                           db_file=db_file, peer_file=peer_file)
  
	def hello(self, address: str, port: int):
		self._engine.hello(address=address, port=port)
  
	def shutdown(self) -> None:
		self._engine.shutdown()
  
	def follow(self, uid: str) -> None:
		self._local_user.follow(uid)
  
	def getFollows(self) -> list[str]:
		return self._local_user.getFollows()

	def _createUser(self, nickname: str) -> tuple[str, str]:
		
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

		return (uid, pubkey_str)

	def writePost(self, text: str) -> None:
		
		author = self._local_user.getUid()
  
		privkey = self._local_user.getPrivkey()
		signature = rsa.sign(
      			text.encode(), privkey, "SHA-256"
        ).hex()
  
		self._engine.handleData(
			[{
				"type": "post",
				"author": author,
				"text": text,
				"signature": signature,
				"uid": None
			}]
		)

	def getPosts(self, uid: str) -> list:
		
		posts = self._engine.request(
			[{
				"type": "user",
				"uid": uid,
				"posts": []
			}]
		)
  
		posts = posts[0]["posts"]
  
		if len(posts) == 0:
			return []
		else:
			posts = self._engine.request(
				list(map(lambda x: {"uid": x, "type": "post", "text": None}, posts))
			)
			return posts

if __name__ == "__main__":
	
	pass

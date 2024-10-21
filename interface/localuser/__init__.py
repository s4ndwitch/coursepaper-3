
from rsa import PublicKey, PrivateKey

import json

class LocalUser:
	
	_config_file: str

	def __init__(self, config_file: str = "./localuser.ini") -> None:

		self._config_file = config_file
		open(config_file, "a").close()
		data = open(config_file, "r").read()
		if len(data) == 0:
			open(config_file, "w").write("{}")

	def setUser(self, privkey: PrivateKey, pubkey: PublicKey, uid: str) -> None:
		
		config = json.loads(open(self._config_file, "r").read())
		config["user"] = {
			"uid": uid,
			"pubkey": pubkey.save_pkcs1().decode(),
			"privkey": privkey.save_pkcs1().decode()
		}
		open(self._config_file, "w").write(json.dumps(config))

	def getPrivkey(self) -> PrivateKey:
     
		config = json.loads(open(self._config_file, "r").read())
	 
		return PrivateKey.load_pkcs1(config["user"]["privkey"])

	def getPubkey(self) -> PublicKey:
     
		config = json.loads(open(self._config_file, "r").read())

		return PublicKey.load_pkcs1(config["user"]["pubkey"])

	def getUid(self) -> str:
     
		config = json.loads(open(self._config_file, "r").read())

		return PublicKey.load_pkcs1(config["user"]["uid"])

	def follow(self, uid: str) -> None:
     
		config = json.loads(open(self._config_file, "r").read())
  
		if "follows" not in config.keys():
			config["follows"] = list()
  
		if uid not in config["follows"]:
			config["follows"] += [uid]
   
		open(self._config_file, "w").write(json.dumps(config))

	def getFollows(self) -> list[str]:
     
		config = json.loads(open(self._config_file, "r").read())
  
		return config["follows"] if "follows" in config.keys() else []

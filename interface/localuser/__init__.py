
from configparser import ConfigParser
from rsa import PublicKey, PrivateKey

class LocalUser:

	def __init__(self, config_file: str = "./localuser.ini") -> None:

		self._config: ConfigParser = ConfigParser()
		self._config.read(config_file)

	def setPrivkey(self, privkey: PrivateKey) -> None:
		
		self._config["privkey"] = privkey.save_pkcs1()

	def setPubKey(self, pubkey: PublicKey) -> None:
		
		self._config["pubkey"] = pubkey.save_pkcs1()

	def setUid(self, uid: str) -> None:
		
		self._config["uid"] = uid

	def getPrivkey(self) -> PrivateKey:
     
		return PrivateKey.load_pkcs1(self._config["privkey"])

	def getPubkey(self) -> PublicKey:

		return PublicKey.load_pkcs1(self._config["pubkey"])

	def getUid(self) -> str:
		
		return self._config["uid"]

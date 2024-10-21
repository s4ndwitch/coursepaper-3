
from interface import Interface
interface = Interface()
interface.createUser("qwerty")

interface.follow("91aace45e2a5f91073709e0f3bdafb1d82bc3679a8f64a3106dd00a8fe8c90fd")
print(interface.getFollows())

interface.writePost("test")

interface.shutdown()

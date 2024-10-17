
class Follow:

    _signature: str
    _who: str
    _whom: str
    
    def __init__(self, signature: str, who: str, whom: str) -> None:
    
        self._signature = signature
        self._who = who
        self._whom = whom

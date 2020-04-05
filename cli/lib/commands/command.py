from lib import client
from typing import List, Any

class Command(object):
    def __init__(self, client: client.Client) -> None:
        self.cl: client.Client = client

    def exec(self, args: List[str]) -> None:
        raise NotImplementedError
    
    def compl(self, text: str) -> Any:
        return None
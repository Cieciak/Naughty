from .dummy import DummyClient
from .R34 import Rule34
from ..post import Post

class Client:
    def get_posts(self, tags: list[str], **kwagrs) -> list[Post]: ...

available_clients: list[Client]  = [Rule34]
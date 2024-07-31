from dataclasses import dataclass

@dataclass
class Post:
    sample_url: str
    file_url: str
    tags: str
    id: int
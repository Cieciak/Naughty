import requests
import os

from pprint import pprint
from ..post import Post

class e621:
    PAGE_SIZE = 100
    POSTS = 'https://e621.net/posts.json'

    def __init__(self):
        ...

    def get_posts(self, tags: list[str], page: int = 0, limit: int = None) -> list[Post]:
        # Set limit for posts
        if limit is None: limit = self.PAGE_SIZE

        # Send API request
        response = requests.get(
            self.POSTS,
            params={'tags': ' '.join(tags), 'limit': limit, 'page': page},
            headers={'User-agent': f'Capp-{os.getlogin()}/0.1'}
        )

        results = []
        for post in response.json()['posts']:

            tags = []
            tags += post['tags']['artist']
            tags += post['tags']['character']
            tags += post['tags']['copyright']
            tags += post['tags']['general']
            tags += post['tags']['lore']
            tags += post['tags']['meta']
            tags += post['tags']['species']

            kwargs = {
                'sample_url': post['sample']['url'],
                'source': self.__class__.__name__,
                'file_url': post['file']['url'],
                'tags': tags,
                'id': post['id'],
            }
            results.append(Post(**kwargs))

        return results
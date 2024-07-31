import requests
from xml.etree import ElementTree

from ..post import Post

class Rule34:
    PAGE_SIZE = 100
    POSTS = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index'

    def __init__(self):
        ...
    
    def get_posts(self, tags: list[str], limit: int = None, page: int = 0) -> list[Post]:
        # Set limit for posts
        if limit is None: limit = self.PAGE_SIZE

        # Send request to Rule34 API
        response = requests.get(self.POSTS, params = {'tags': ' '.join(tags), 'limit': limit, 'pid': page})
        root = ElementTree.fromstring(response.text)

        # Iterate over XML to get all post data
        results: list[Post] = []
        for post in root.findall('post'):
            kwargs = {
                'sample_url': post.get('sample_url'),
                'file_url':   post.get('file_url'),
                'tags':       post.get('tags'),
                'id':         post.get('id'),
            }
            results.append(Post(**kwargs))


        return results   
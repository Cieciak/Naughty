from ..post import Post

class DummyClient:
    COUNT = 50

    def get_posts(self, tags: list[str]) -> list[Post]:
        base = ' '.join(tags)
        
        result: list[Post] = []
        for index in range(self.COUNT):
            kwargs = {
                'file_url': f'[FILE]{base}{index}',
                'sample_url': f'[SAMPLE]{base}{index}',
                'tags': tags,
                'id': hash(base) + index,
            }
            result.append(Post(**kwargs))

        return result
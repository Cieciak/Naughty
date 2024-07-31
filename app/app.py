import tkinter as tk
from .clients import available_clients, Client
from .post import Post
from .config import open_config

import os.path
import requests
from PIL import Image, ImageTk
from io import BytesIO, FileIO

class Application:
    MAX_HEIGHT = 800

    def __init__(self, home: str = ''):
        self.clients: list[Client] = []
        self.current: Post = None
        self.posts: list[Post] = []
        self.root = tk.Tk()
        self.home: str = home
        self.tags: list[str] = []
        self.page: int = 0

        self.next_button = tk.Button(master=self.root, text='Config', command=lambda: open_config(self))
        self.next_button.grid(row=0, column=0)

        self.next_button = tk.Button(master=self.root, text='Refresh', command=lambda: (self.get_posts(self.tags), self.next_image()))
        self.next_button.grid(row=0, column=1)

        self.next_button = tk.Button(master=self.root, text='Next', command=self.next_image)
        self.next_button.grid(row=1, column=0)

        self.next_button = tk.Button(master=self.root, text='Save', command=self.save_image)
        self.next_button.grid(row=1, column=1)

        self.next_button = tk.Button(master=self.root, text='Save tags', command=self.save_tags)
        self.next_button.grid(row=1, column=2)

        self.image = tk.Label(master=self.root)
        self.image.grid(row=2, columnspan=1000, rowspan=20)

        self.posts_counter = tk.Label(self.root)
        self.posts_counter.grid(row=23, column=0)

        self.page_counter = tk.Label(self.root)
        self.page_counter.grid(row=23, column=1)

        self.init_clients()
        self.get_posts(self.tags)

        self.next_image()

        self.root.mainloop()

    def init_clients(self, configs: dict = {}):
        for client_class in available_clients:
            if client_class in configs:
                client_instance = client_class(**configs[client_class])
            else:
                client_instance = client_class()
            self.clients.append(client_instance)

    def get_posts(self, tags: list[str] = [], **kwargs) -> list[Post]:
        print(tags)
        gathered: list[Post] = []
        for client in self.clients:
            gathered += client.get_posts(tags, **kwargs)

        self.posts = gathered
        return self.posts
    
    def next_image(self):

        # Do not show mp4
        extension = None
        while extension in ['mp4', None]:
            self.current = self.posts.pop(0)
            *_, extension = self.current.file_url.split('.')

        # Download image
        buffer = BytesIO(requests.get(self.current.sample_url).content)
        pillow = Image.open(buffer)

        # Resize image to fit
        width, height = pillow.size
        if height > self.MAX_HEIGHT:
            width *= self.MAX_HEIGHT / height
            height = self.MAX_HEIGHT
        pillow = pillow.resize((int(width), height))

        tk_image = ImageTk.PhotoImage(pillow)
        self.image.config(image=tk_image)
        self.image.tk_image = tk_image # Prevent garbage collection

        self.posts_counter.config(text=f'Posts left: {len(self.posts)}')
        self.page_counter.config(text=f'Page: {self.page}')
        if len(self.posts) == 0:
            self.page += 1
            self.get_posts(self.tags, page=self.page)

    def save_image(self):
        # File extension
        *_, extension = self.current.file_url.split('.')

        # Generate path
        name = f'{self.current.id}.{extension}'
        path = os.path.join(self.home, name)

        # Get image data
        data = requests.get(self.current.file_url).content

        # Save image
        with open(path, 'wb') as file: file.write(data)

        self.next_image()


    def save_tags(self):

        # Generate path
        name = f'{self.current.id}.tag'
        path = os.path.join(self.home, name)

        with open(path, 'w') as file:
            data = self.current.tags.strip().replace(' ', '\n')
            file.write(data)

    def update_state(self, data: dict):
        for key, val in data.items():
            setattr(self, key, val)
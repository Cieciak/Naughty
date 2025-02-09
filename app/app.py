import tkinter as tk
from .clients import available_clients, Client
from .post import Post
from .config import open_config
from .queue import PostQueue

import os.path
import requests
from PIL import Image, ImageTk
from io import BytesIO
from pprint import pprint

class Application:
    MAX_WIDTH  = 800
    MAX_HEIGHT = 800

    EXCLUDED_EXT = ['mp4']

    DEFAULT_BG = '#1c1d21'
    BUTTON = '#323135'
    LIGHT_BUTTON = '#3c3b40'
    DEFAULT_TX = '#bb9bb0'
    LIGHT_BG = '#26272c'
    GREEN = '#1d3223'
    LIGHT_GREEN = '#25412d'
    RED = '#4C1C1F'
    LIGHT_RED = '#592125'
    TEXT = '#CCBCBC'
    LIGHT_TEXT = '#DCD0D0'

    button_cnf = {
        'highlightthickness': 0,
        'borderwidth': 0,
        'padx': 0,
        'pady': 0,
        'font': ('Lato', 16),

        'background': BUTTON,
        'activebackground': LIGHT_BUTTON,

        'foreground': TEXT,
        'activeforeground': LIGHT_TEXT,
    }

    label_cnf = {
        'background': DEFAULT_BG,
        'foreground': TEXT,

        'font': ('Lato', 16)
    }


    def __init__(self, home: str = ''):


        self.clients: list[Client] = []
        self.current: Post = None
        self.root = tk.Tk()
        self.home: str = home
        self.page: int = 0

        self.tags: list[str] = list()

        self.queue: PostQueue = PostQueue(target=10)

        self.textvars: dict[str, tk.StringVar] = {
            'tags': tk.StringVar(self.root),
        }

        self.root.geometry(f'{160+self.MAX_WIDTH}x{150+self.MAX_HEIGHT}')
        self.root.configure(background=self.DEFAULT_BG)

        # CONFIG Button
        self.config_button = tk.Button(
            cnf=self.button_cnf,
            master=self.root,
            text='Config',
            command=lambda: open_config(self),
        )
        self.config_button.place(
            x=0,
            y=0,
            width=80,
            height=50,
        )

        # REFRESH Button
        self.refresh_button = tk.Button(
            cnf=self.button_cnf,
            master=self.root,
            text='Refresh',
            command=lambda: (self.queue.flush(), self.get_posts(self.tags), self.next_image()),
        )
        self.refresh_button.place(
            x=80,
            y=0,
            width=80,
            height=50,
        )

        # No button Button
        self.no_button = tk.Button(
            cnf=self.button_cnf,
            master=self.root,
            text='',
            command=self.next_image,

            background=self.RED,
            activebackground=self.LIGHT_RED,
        )
        self.no_button.place(
            x=0,
            y=100,
            width=80,
            height=self.MAX_HEIGHT,
        )

        self.bk_button = tk.Button(
            cnf=self.button_cnf,
            master=self.root,
            text='',
            command=self.back_image,

            background='#121342',
            activebackground='#222352',
        )
        self.bk_button.place(
            x=0,
            y=100+self.MAX_HEIGHT,
            width=80,
            height=50,
        )

        #Save button
        self.ys_button = tk.Button(
            master=self.root,
            text='',
            command=self.save_image,
            background=self.GREEN,
            activebackground=self.LIGHT_GREEN,
            borderwidth=0,
            padx=0,
            pady=0,
            highlightthickness=0,
        )
        self.ys_button.place(
            x=80+self.MAX_WIDTH,
            y=100,
            width=80,
            height=self.MAX_HEIGHT,
        )

        #Save tags
        self.tags_button = tk.Button(
            cnf=self.button_cnf,
            master=self.root,
            text='Tags',
            command=lambda: self.save_tags(),
        )
        self.tags_button.place(
            x=0,
            y=50,
            width=80,
            height=50,
        )

        # IMAGE
        self.image = tk.Label(
            master=self.root,
            background=self.DEFAULT_BG,
        )
        self.image.place(
            x=80,
            y=100,
            width=self.MAX_WIDTH,
            height=self.MAX_HEIGHT,
        )

        self.taglist_label = tk.Label(
            master=self.root,
            textvariable=self.textvars['tags'],
            anchor='nw',
            justify=tk.LEFT,
            width=100,
            font=('Lato', 12),
            wraplength=self.MAX_WIDTH,
            background=self.DEFAULT_BG,
            foreground=self.TEXT,
        )
        self.taglist_label.place(
            x=80,
            y=50,
            width=self.MAX_WIDTH,
            height=50,
        )

        self.posts_counter = tk.Label(
            master=self.root,
            background=self.DEFAULT_BG,
            foreground=self.DEFAULT_TX,
            font=('Lato', 16)
        )
        self.posts_counter.place(
            x=80,
            y=115+self.MAX_HEIGHT,
            width=80,
            height=35,
        )
        
        self.posts_counter_label = tk.Label(
            master=self.root,
            background=self.DEFAULT_BG,
            foreground=self.TEXT,
            font=('Lato', 10),
            text='Posts',
        )
        self.posts_counter_label.place(
            x=80,
            y=100+self.MAX_HEIGHT,
            width=80,
            height=15, 
        )

        self.page_counter_label = tk.Label(
            master=self.root,
            background=self.DEFAULT_BG,
            foreground=self.TEXT,
            font=('Lato', 10),
            text='Page',
        )
        self.page_counter_label.place(
            x=160,
            y=100+self.MAX_HEIGHT,
            width=80,
            height=15,
        )

        self.page_counter = tk.Label(
            master=self.root,
            background=self.DEFAULT_BG,
            foreground=self.TEXT,
            font=('Lato', 16)
        )
        self.page_counter.place(
            x=160,
            y=115+self.MAX_HEIGHT,
            width=80,
            height=35,
        )

        self.source_label = tk.Label(
            cnf=self.label_cnf,
            master=self.root,
            font=('Lato', 10),
            text='Source'
        )
        self.source_label.place(
            x=240,
            y=100+self.MAX_HEIGHT,
            width=80,
            height=15,
        )

        self.source_field = tk.Label(
            cnf=self.label_cnf,
            master=self.root,
            font=('Lato', 16),
        )
        self.source_field.place(
            x=240,
            y=115+self.MAX_HEIGHT,
            width=80,
            height=35,
        )

        self.ext_label = tk.Label(
            master=self.root,
            background=self.DEFAULT_BG,
            foreground=self.TEXT,
            font=('Lato', 25),
            text='JPEG'
        )
        self.ext_label.place(
            x=80+self.MAX_WIDTH,
            y=50,
            width=80,
            height=50,
        )
        

        self.init_clients()
        self.get_posts(self.tags)

        self.next_image()

    def init_clients(self, configs: dict = {}):
        for client_class in available_clients:
            if client_class in configs:
                client_instance = client_class(**configs[client_class])
            else:
                client_instance = client_class()
            self.clients.append(client_instance)

    def get_posts(self, tags: list[str] = [], **kwargs):
        returned: list[Post] = []
        for client in self.clients:
            returned += client.get_posts(tags, **kwargs)

        gathered: list[Post] = [
            post for post in returned if self.filter_requested(post)
        ]

        self.queue.extend(
            gathered
        )

    @staticmethod
    def filter_requested(post) -> bool:

        # Ignore all post without file_url
        if post.file_url == None: return False

        # Ignore all post with some extensions
        if post.file_url.split('.')[-1] in Application.EXCLUDED_EXT: return False

        return True
    
    def next_image(self):

        self.current = self.queue.pop()

        buffer = BytesIO(requests.get(self.current.sample_url).content)
        pillow = Image.open(buffer)

        # Resize image to fit in the middle
        width, height = pillow.size
        if height > self.MAX_HEIGHT:
            width *= self.MAX_HEIGHT / height
            height = self.MAX_HEIGHT
        if width > self.MAX_WIDTH:
            height *= self.MAX_WIDTH / width
            width   = self.MAX_WIDTH
        pillow = pillow.resize((int(width), int(height)))

        tk_image = ImageTk.PhotoImage(pillow)
        self.image.config(image=tk_image)
        self.image.tk_image = tk_image # Prevent garbage collection

        # Handle updating the GUI
        self.textvars['tags'].set(self.current.tags)
        self.ext_label.config(text=f'{self.current.file_url.split('.')[-1].upper()}')
        self.posts_counter.config(text=f'{self.queue.length}')
        self.page_counter.config(text=f'{self.page}')
        self.source_field.config(text=f'{self.current.source}')

        # Update page
        if self.queue.empty:
            self.page += 1
            self.get_posts(self.tags, page=self.page)

    def back_image(self):
        # Numbers are one bigger because the queue is post incrementing, plus using next_image
        if self.queue.pointer == 1: return
        self.queue.pointer -= 2
        self.next_image()

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

    def start(self):
        self.root.mainloop()
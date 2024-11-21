import tkinter as tk
from .clients import available_clients, Client
from .post import Post
from .config import open_config

import os.path
import requests
from PIL import Image, ImageTk
from io import BytesIO, FileIO

class Application:
    MAX_WIDTH  = 800
    MAX_HEIGHT = 800

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



    def __init__(self, home: str = ''):


        self.clients: list[Client] = []
        self.current: Post = None
        self.posts: list[Post] = []
        self.root = tk.Tk()
        self.home: str = home
        self.tags: list[str] = []
        self.page: int = 0

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
            command=lambda: (self.get_posts(self.tags), self.next_image()),
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
            command=lambda: print('Get tags'),
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
            x=0,
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
            x=0,
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
            x=80,
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
            x=80,
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
        pillow = pillow.resize((int(width), int(height)))
        if width > self.MAX_WIDTH:
            height *= self.MAX_WIDTH / width
            width   = self.MAX_WIDTH
        pillow = pillow.resize((int(width), int(height)))

        tk_image = ImageTk.PhotoImage(pillow)
        self.image.config(image=tk_image)
        self.image.tk_image = tk_image # Prevent garbage collection

        self.textvars['tags'].set(self.current.tags)

        self.ext_label.config(text=f'{extension.upper()}')
        self.posts_counter.config(text=f'{len(self.posts)}')
        self.page_counter.config(text=f'{self.page}')
        if len(self.posts) == 0:
            self.page += 1
            self.posts = self.get_posts(self.tags, page=self.page)

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
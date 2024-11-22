import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfile

BACKGROUND = '#1c1d21'
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

entry_cnf = {
    'highlightthickness': 0,
    'borderwidth': 0,
    'font': ('Lato', 16),

    'background': BUTTON,
    'foreground': TEXT,
}

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

def open_config(app):
    root = tk.Toplevel(app.root)
    
    root.title('Config')
    root.geometry(f'{880+40}x{150}')
    root.configure(background=BACKGROUND)

    tag_variable = tk.StringVar(root)
    dir_variable = tk.StringVar(root)

    tag_variable.set(app.tags)
    dir_variable.set(app.home)
    
    tag_label = tk.Label(
        master=root,
        text='Tags:',
        font=('Lato', 16),
        
        background=BACKGROUND,
        foreground=TEXT,
    )
    tag_label.place(
        x=0,
        y=0,
        width=80,
        height=50,
    )
    
    tag_entry = tk.Entry(
        cnf=entry_cnf,
        master=root,
        textvariable=tag_variable,
        font=('Lato', 16),
        background=BUTTON,
    )
    tag_entry.place(
        x=80,
        y=0,
        width=800,
        height=50,
    )

    tag_ask = tk.Button(
        cnf=button_cnf,
        master=root,
        text='...',
        command=lambda: get_tagfile(),
    )
    tag_ask.place(
        x=880,
        y=0,
        width=40,
        height=50,
    )

    dir_label = tk.Label(
        master=root,
        text='Path:',
        font=('Lato', 16),
        
        background=BACKGROUND,
        foreground=TEXT,
    )
    dir_label.place(
        x=0,
        y=50,
        width=80,
        height=50,
    )

    dir_entry = tk.Entry(
        cnf=entry_cnf,
        master=root,
        textvariable=dir_variable,
        font=('Lato', 16),
        background=BUTTON,
    )
    dir_entry.place(
        x=80,
        y=50,
        width=800,
        height=50,
    )
    dir_ask = tk.Button(
        cnf=button_cnf,
        master=root,
        text='...',
        command=lambda: get_directory(),
    )
    dir_ask.place(
        x=880,
        y=50,
        width=40,
        height=50,
    )

    save_exit_button = tk.Button(
        cnf=button_cnf,
        master=root,
        text='Save and Exit',
        command=lambda: save(),
    )
    save_exit_button.place(
        x=0,
        y=100,
        width=160,
        height=50,
    )

    def save():
        data = {
            'home': dir_variable.get(),
            'tags': tag_variable.get().strip().split(' ')
        }
        app.page = 0
        app.update_state(data)
        
        root.destroy()

    def get_directory():
        path = askdirectory(mustexist=False)
        dir_variable.set(path)

    def get_tagfile():
        file = askopenfile(defaultextension='tag')
        tags = ' '.join(file.read().split('\n'))
        tag_variable.set(tags)
        file.close()
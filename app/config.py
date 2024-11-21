import tkinter as tk

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

def open_config(app):
    config_tk = tk.Toplevel(app.root)
    config_tk.title('Config')
    config_tk.configure(background=BACKGROUND)

    tag_var = tk.StringVar(config_tk)
    dir_var = tk.StringVar(config_tk)

    tag_label = tk.Label(
        master=config_tk,
        text='Tags:',
        height=2,
        width=10,
    )
    tag_label.grid(row=0, column=0)

    tag_entry = tk.Entry(
        master=config_tk,
        textvariable=tag_var,
        width=100,
    )
    tag_entry.grid(row=0, column=1, columnspan=10)

    dir_label = tk.Label(
        config_tk,
        text='Directory:',
        height=2,
        width=10,
    )
    dir_label.grid(row=1, column=0)

    dir_entry = tk.Entry(
        config_tk,
        textvariable=dir_var,
        width=100
    )
    dir_entry.grid(row=1, column=1, columnspan=10)

    save_button = tk.Button(
        config_tk,text='Save',
        command=lambda: save({'home': dir_var.get(), 'tags': tag_var.get().strip().split(' ')}, False)
    )
    save_button.grid(row=2, column=0)

    save_exit_button = tk.Button(
        config_tk,
        text='Save and Exit',
        command=lambda: save({'home': dir_var.get(), 'tags': tag_var.get().strip().split(' ')}, True)
    )
    save_exit_button.grid(row=2, column=1)

    def save(data: dict, exit: bool = False):
        app.page = 0
        app.update_state(data)
        if exit: config_tk.destroy()
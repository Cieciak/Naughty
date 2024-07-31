import tkinter as tk

def open_config(app):
    config_tk = tk.Toplevel(app.root)
    config_tk.title('Config')

    tag_var = tk.StringVar(config_tk)
    dir_var = tk.StringVar(config_tk)

    tag_label = tk.Label(config_tk, text='Tags:')
    tag_label.grid(row=0, column=0)

    tag_entry = tk.Entry(config_tk, textvariable=tag_var, width=100)
    tag_entry.grid(row=0, column=1)

    dir_label = tk.Label(config_tk, text='Directory:')
    dir_label.grid(row=1, column=0)

    dir_entry = tk.Entry(config_tk, textvariable=dir_var, width=100)
    dir_entry.grid(row=1, column=1)

    save_button = tk.Button(config_tk, text='Save', command=lambda: save({'home': dir_var.get(), 'tags': tag_var.get().strip().split(' ')}, False))
    save_button.grid(row=2, column=0)

    save_exit_button = tk.Button(config_tk, text='Save and Exit', command=lambda: save({'home': dir_var.get(), 'tags': tag_var.get().strip().split(' ')}, True))
    save_exit_button.grid(row=2, column=1)

    def save(data: dict, exit: bool = False):
        app.page = 0
        app.update_state(data)
        if exit: config_tk.destroy()
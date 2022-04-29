# coding=utf-8
import time
import os
import sys
import subprocess
import tink
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

PY2 = sys.version_info[0] == 2
APP_HEIGHT = 350
APP_WIDTH = 700
APP_NAME = 'Tool - PhiDinhTuAnh - AT140402'


class Reloader(object):

    RELOADING_CODE = 3

    def start_process(self):
        """Spawn a new Python interpreter with the same arguments as this one,
        but running the reloader thread.
        """
        while True:
            print("starting Tkinter application...")

            args = [sys.executable] + sys.argv
            env = os.environ.copy()
            env['TKINTER_MAIN'] = 'true'

            if os.name == 'nt' and PY2:
                for key, value in env.iteritems():
                    if isinstance(value, unicode):
                        env[key] = value.encode('iso-8859-1')

            exit_code = subprocess.call(args, env=env,
                                        close_fds=False)
            if exit_code != self.RELOADING_CODE:
                return exit_code

    def trigger_reload(self):
        self.log_reload()
        sys.exit(self.RELOADING_CODE)

    def log_reload(self):
        print("reloading...")


def run_with_reloader(root, *hotkeys):
    """Run the given application in an independent python interpreter."""
    import signal
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    reloader = Reloader()
    try:
        if os.environ.get('TKINTER_MAIN') == 'true':

            for hotkey in hotkeys:
                root.bind_all(hotkey, lambda event: reloader.trigger_reload())

            # if os.name == 'nt':
            #     root.wm_state("iconic")
            #     root.wm_state("zoomed")

            root.mainloop()
        else:
            sys.exit(reloader.start_process())
    except KeyboardInterrupt:
        pass


def center_screen(root):
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (APP_WIDTH/2))
    y_cordinate = int((screen_height/2) - (APP_HEIGHT/2))

    # Hiển thị giữa màn hình
    root.geometry("{}x{}+{}+{}".format(APP_WIDTH,
                  APP_HEIGHT, x_cordinate, y_cordinate))


def create_tab(root):
    tabControl = ttk.Notebook(root)

    tab1 = Frame(tabControl)
    tab2 = Frame(tabControl)
    tab3 = Frame(tabControl)

    tabControl.add(tab1, text='Key generation')
    tabControl.add(tab2, text='Encryption')
    tabControl.add(tab3, text='Decryption')
    tabControl.pack(expand=1, fill="both")

    key_generation(tab1)
    encryption(tab2)
    decryption(tab3)


def key_generation(root):
    seedLabel = Label(root, text="Seed")
    seedLabel.grid(row=0)
    seedInput = Entry(root)
    seedInput.grid(column=1, row=0)

    def generate():
        print(seedInput.get())

    genKeyBtn = Button(root, text='Gen Key', command=generate)
    genKeyBtn.grid(row=1, column=1, pady=4)

    keyLabel = Label(root, text="Key")
    keyLabel.grid(row=2)
    keyInput = Entry(root)
    keyInput.grid(column=1, row=2)


def encryption(root):
    plaintextLabel = Label(root, text="Plaintext")
    plaintextLabel.grid(row=0)
    plaintextInput = Entry(root)
    plaintextInput.grid(row=0, column=1)

    def browse_func():
        filename = filedialog.askopenfilename()
        plaintextInput.insert(END, filename)

    openFileBtn = Button(root, text="Open file", command=browse_func)
    openFileBtn.grid(row=0, column=2, pady=4, padx=4)

    keyLabel = Label(root, text="Key")
    keyLabel.grid(row=1)
    keyInput = Entry(root)
    keyInput.grid(column=1, row=1)

    def encryption():
        print(plaintextInput.get())

    encryptionBtn = Button(root, text="Encryption", command=encryption)
    encryptionBtn.grid(row=2, column=0, pady=4, padx=4)

    cipherTextLabel = Label(root, text="CipherText")
    cipherTextLabel.grid(row=3)
    cipherTextInput = Entry(root)
    cipherTextInput.grid(column=1, row=3)


def decryption(root):
    cipherTextLabel = Label(root, text="Ciphertext")
    cipherTextLabel.grid(row=0)
    cipherTextInput = Entry(root)
    cipherTextInput.grid(row=0, column=1)

    def browse_func():
        filename = filedialog.askopenfilename()
        cipherTextInput.insert(END, filename)

    openFileBtn = Button(root, text="Open file", command=browse_func)
    openFileBtn.grid(row=0, column=2, pady=4, padx=4)

    keyLabel = Label(root, text="Key")
    keyLabel.grid(row=1)
    keyInput = Entry(root)
    keyInput.grid(column=1, row=1)

    def decryption():
        print(plaintextInput.get())

    decryptionBtn = Button(root, text="Decryption", command=decryption)
    decryptionBtn.grid(row=2, column=0, pady=4, padx=4)

    plaintextLabel = Label(root, text="Plaintext")
    plaintextLabel.grid(row=3)
    plaintextInput = Entry(root)
    plaintextInput.grid(column=1, row=3)


if __name__ == "__main__":
    win = Tk()
    win.title(APP_NAME)

    center_screen(win)

    create_tab(win)

    run_with_reloader(win, "<Control-R>", "<Control-r>")

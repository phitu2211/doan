# coding=utf-8
import time
import binascii
import os
import sys
import subprocess
import tink
from tink import aead
from tink import signature
from tink import cleartext_keyset_handle
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
PY2 = sys.version_info[0] == 2
APP_HEIGHT = 240
APP_WIDTH = 500
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
    tab4 = Frame(tabControl)
    tab5 = Frame(tabControl)

    tabControl.add(tab1, text='Key generation')
    tabControl.add(tab2, text='Encryption')
    tabControl.add(tab3, text='Decryption')
    tabControl.add(tab4, text='Sign')
    tabControl.add(tab5, text='Verify')
    tabControl.pack(expand=True, fill="both")

    key_generation(tab1)
    encryption(tab2)
    decryption(tab3)
    sign(tab4)
    verify(tab5)


def key_generation(root):
    def generate_ds():
        try:
            key_template = signature.signature_key_templates.ECDSA_P256
            keyset_handle = tink.KeysetHandle.generate_new(key_template)
        except tink.TinkError as e:
            print('Error creating primitive')
            print(e)

        files = [('json', '*.json')]
        file = filedialog.asksaveasfile(filetypes=files, defaultextension=files, initialfile="signature_private")

        with open(file.name, 'wt') as keyset_file:
            try:
                cleartext_keyset_handle.write(
                    tink.JsonKeysetWriter(keyset_file), keyset_handle)

            except tink.TinkError as e:
                print('Error writing key')
                print(e)

        try:
            keyset_handle = keyset_handle.public_keyset_handle();
        except tink.TinkError as e:
            print('Error creating primitive')
            print(e)

        files = [('json', '*.json')]
        file = filedialog.asksaveasfile(filetypes=files, defaultextension=files, initialfile="signature_public")

        with open(file.name, 'wt') as keyset_file:
            try:
                cleartext_keyset_handle.write(
                    tink.JsonKeysetWriter(keyset_file), keyset_handle)

            except tink.TinkError as e:
                print('Error writing key')
                print(e)

    def generate():
        try:
            key_template = aead.aead_key_templates.AES128_GCM
            keyset_handle = tink.KeysetHandle.generate_new(key_template)
        except tink.TinkError as e:
            print('Error creating primitive')
            print(e)

        files = [('json', '*.json')]
        file = filedialog.asksaveasfile(filetypes=files, defaultextension=files, initialfile="aead_key")

        with open(file.name, 'wt') as keyset_file:
            try:
                cleartext_keyset_handle.write(
                    tink.JsonKeysetWriter(keyset_file), keyset_handle)

            except tink.TinkError as e:
                print('Error writing key')
                print(e)

    genKeyBtn = Button(root, text='Gen Key AEAD', command=generate)
    genKeyBtn.grid(row=1, column=1, pady=4)
    genKeyDsBtn = Button(root, text='Gen Key Digital Signature', command=generate_ds)
    genKeyDsBtn.grid(row=2, column=1, pady=4)


def encryption(root):
    plaintextLabel = Label(root, text="Plaintext")
    plaintextLabel.grid(row=0)
    plaintextInput = Entry(root)
    plaintextInput.grid(row=0, column=1)

    def open_plain_file():
        plaintextInput.delete(0, END)
        filename = filedialog.askopenfilename()
        plaintextInput.insert(END, filename)

    openFileBtn = Button(root, text="Open file", command=open_plain_file)
    openFileBtn.grid(row=0, column=2, pady=4, padx=4)

    keyLabel = Label(root, text="Key")
    keyLabel.grid(row=1)
    keyInput = Entry(root)
    keyInput.grid(column=1, row=1)

    def open_key_file():
        keyInput.delete(0, END)
        filename = filedialog.askopenfilename()
        keyInput.insert(END, filename)

    openFileBtn = Button(root, text="Open key", command=open_key_file)
    openFileBtn.grid(row=1, column=2, pady=4, padx=4)

    def encryption():
        associated_data = b''

        cipher = get_cipher(keyInput.get(), aead.Aead)

        with open(plaintextInput.get(), 'rb') as input_file:
            input_data = input_file.read()
            output_data = cipher.encrypt(input_data, associated_data)

        files = [('All Files', '*.*')]
        file = filedialog.asksaveasfile(
            filetypes=files, defaultextension=files)
        with open(file.name, 'wb') as output_file:
            output_file.write(output_data)

    encryptionBtn = Button(root, text="Encryption", command=encryption)
    encryptionBtn.grid(row=2, column=1, pady=4, padx=4)


def decryption(root):
    cipherTextLabel = Label(root, text="Ciphertext")
    cipherTextLabel.grid(row=0)
    cipherTextInput = Entry(root)
    cipherTextInput.grid(row=0, column=1)

    def open_cipher_file():
        cipherTextInput.delete(0, END)
        filename = filedialog.askopenfilename()
        cipherTextInput.insert(END, filename)

    openFileBtn = Button(root, text="Open file", command=open_cipher_file)
    openFileBtn.grid(row=0, column=2, pady=4, padx=4)

    keyLabel = Label(root, text="Key")
    keyLabel.grid(row=1)
    keyInput = Entry(root)
    keyInput.grid(column=1, row=1)

    def open_key_file():
        keyInput.delete(0, END)
        filename = filedialog.askopenfilename()
        keyInput.insert(END, filename)

    openFileBtn = Button(root, text="Open key", command=open_key_file)
    openFileBtn.grid(row=1, column=2, pady=4, padx=4)

    def decryption():
        associated_data = b''

        cipher = get_cipher(keyInput.get(), aead.Aead)

        with open(cipherTextInput.get(), 'rb') as input_file:
            input_data = input_file.read()
            output_data = cipher.decrypt(input_data, associated_data)

        files = [('All Files', '*.*')]
        file = filedialog.asksaveasfile(
            filetypes=files, defaultextension=files)
        with open(file.name, 'wb') as output_file:
            output_file.write(output_data)

    decryptionBtn = Button(root, text="Decryption", command=decryption)
    decryptionBtn.grid(row=2, column=1, pady=4, padx=4)

def verify(root):
    cipherTextLabel = Label(root, text="File")
    cipherTextLabel.grid(row=0)
    cipherTextInput = Entry(root)
    cipherTextInput.grid(row=0, column=1)

    signatureLabel = Label(root, text="Signature")
    signatureLabel.grid(row=2)
    signatureInput = Entry(root)
    signatureInput.grid(row=2, column=1)

    def open_signature_file():
        signatureInput.delete(0, END)
        filename = filedialog.askopenfilename()
        signatureInput.insert(END, filename)

    openFileBtn = Button(root, text="Open signature file", command=open_signature_file)
    openFileBtn.grid(row=2, column=2, pady=4, padx=4)

    text = StringVar();
    text.set("");

    resultLabel = Label(root, text='Result: ')
    resultLabel.grid(row=4, column=0)
    signatureLabel = Label(root, textvariable=text)
    signatureLabel.grid(row=4, column=1)

    def open_cipher_file():
        cipherTextInput.delete(0, END)
        filename = filedialog.askopenfilename()
        cipherTextInput.insert(END, filename)

    openFileBtn = Button(root, text="Open file", command=open_cipher_file)
    openFileBtn.grid(row=0, column=2, pady=4, padx=4)

    keyLabel = Label(root, text="Public key")
    keyLabel.grid(row=1)
    keyInput = Entry(root)
    keyInput.grid(column=1, row=1)

    def open_key_file():
        keyInput.delete(0, END)
        filename = filedialog.askopenfilename()
        keyInput.insert(END, filename)

    openFileBtn = Button(root, text="Open key", command=open_key_file)
    openFileBtn.grid(row=1, column=2, pady=4, padx=4)

    def verify():
        text.set("");

        cipher = get_cipher(keyInput.get(), signature.PublicKeyVerify)

        with open(cipherTextInput.get(), 'rb') as input_file:
            input_data = input_file.read()

        with open(signatureInput.get(), 'rb') as signature_file:
            try:
              expected_signature = binascii.unhexlify(signature_file.read().strip())
            except binascii.Error as e:
              print('Error reading expected code')
              print(e)

        try:
            cipher.verify(expected_signature, input_data)
            text.set("Success");
        except binascii.Error as e:
            print("Error reading expected signature")
            print(e)
        except tink.TinkError as e:
            text.set("Signature verification failed");
            print(e)

    verifyBtn = Button(root, text="Verify", command=verify)
    verifyBtn.grid(row=3, column=1, pady=4, padx=4)

def sign(root):
    plaintextLabel = Label(root, text="File")
    plaintextLabel.grid(row=0)
    plaintextInput = Entry(root)
    plaintextInput.grid(row=0, column=1)

    def open_plain_file():
        plaintextInput.delete(0, END)
        filename = filedialog.askopenfilename()
        plaintextInput.insert(END, filename)

    openFileBtn = Button(root, text="Open file", command=open_plain_file)
    openFileBtn.grid(row=0, column=2, pady=4, padx=4)

    keyLabel = Label(root, text="Private key")
    keyLabel.grid(row=1)
    keyInput = Entry(root)
    keyInput.grid(column=1, row=1)
    

    def open_key_file():
        keyInput.delete(0, END)
        filename = filedialog.askopenfilename()
        keyInput.insert(END, filename)

    openFileBtn = Button(root, text="Open key", command=open_key_file)
    openFileBtn.grid(row=1, column=2, pady=4, padx=4)

    def sign():
        cipher = get_cipher(keyInput.get(), signature.PublicKeySign)

        with open(plaintextInput.get(), 'rb') as input_file:
            input_data = input_file.read()
            output_data = cipher.sign(input_data)
        
        files = [('All Files', '*.*')]
        file = filedialog.asksaveasfile(
            filetypes=files, defaultextension=files, initialfile="signature")
        with open(file.name, 'wb') as output_file:
            output_file.write(binascii.hexlify(output_data))

    signBtn = Button(root, text="Sign", command=sign)
    signBtn.grid(row=2, column=1, pady=4, padx=4)


def save_file():
    files = [('All Files', '*.*')]
    file = filedialog.asksaveasfile(
        filetypes=files, defaultextension=files)
    return file


def get_cipher(path, primitive):
    with open(path, 'rt') as keyset_file:
        try:
            text = keyset_file.read()
            keyset_handle = cleartext_keyset_handle.read(
                tink.JsonKeysetReader(text))
        except tink.TinkError as e:
            print('Error reading key:')
            print(e)

    try:
        cipher = keyset_handle.primitive(primitive)
    except tink.TinkError as e:
        print('Error creating primitive')
        print(e)

    return cipher


def init_lib():
    try:
        aead.register()
        signature.register()
    except tink.TinkError as e:
        print('Error initialising Tink: %s', e)


if __name__ == "__main__":
    win = Tk()
    win.title(APP_NAME)

    center_screen(win)

    init_lib()

    create_tab(win)

    run_with_reloader(win, "<Control-R>", "<Control-r>")

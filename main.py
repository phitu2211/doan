# coding=utf-8
import time
import os
import sys
import subprocess

PY2 = sys.version_info[0] == 2


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

            # a weird bug on windows. sometimes unicode strings end up in the
            # environment and subprocess.call does not like this, encode them
            # to latin1 and continue.
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

            if os.name == 'nt':
                root.wm_state("iconic")
                root.wm_state("zoomed")

            root.mainloop()
        else:
            sys.exit(reloader.start_process())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    from tkinter import Tk, Label

    class App(Tk):
        def __init__(self):
            Tk.__init__(self)

            self.title("Mã hóa")
            self.resizable(False, False)

            window_height = 500
            window_width = 900

            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            x_cordinate = int((screen_width/2) - (window_width/2))
            y_cordinate = int((screen_height/2) - (window_height/2))

            # Hiển thị giữa màn hình
            self.geometry("{}x{}+{}+{}".format(window_width,
                          window_height, x_cordinate, y_cordinate))

    run_with_reloader(App(), "<Control-R>", "<Control-r>")

# class App:
#     def __init__(self, parent):
#         btn = Button(
#             win,
#             text="Exit",
#             command=win.destroy,
#             background='#48483E',
#             foreground='#CFD0C2'
#         )
#         btn.place(x=80, y=100)


# if __name__ == '__main__':
#     win = Tk()
#     win.resizable(False, False)
#     win.title("Mã hóa")

#     window_height = 500
#     window_width = 900

#     screen_width = win.winfo_screenwidth()
#     screen_height = win.winfo_screenheight()

#     x_cordinate = int((screen_width/2) - (window_width/2))
#     y_cordinate = int((screen_height/2) - (window_height/2))

#     # Hiển thị giữa màn hình
#     win.geometry("{}x{}+{}+{}".format(window_width,
#                  window_height, x_cordinate, y_cordinate))
#     App(win)
#     win.configure(background='white')
#     win.mainloop()

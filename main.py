# coding=utf-8
try:
    from tkinter import *
except ImportError:
    from Tkinter import *


class App:
    def __init__(self, parent):
        btn = Button(
            win,
            text="Exit",
            command=win.destroy,
            background='#48483E',
            foreground='#CFD0C2'
        )
        btn.place(x=80, y=100)


if __name__ == '__main__':
    win = Tk()
    win.resizable(False, False)
    win.title("Mã hóa")

    window_height = 500
    window_width = 900

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    # Hiển thị giữa màn hình
    win.geometry("{}x{}+{}+{}".format(window_width,
                 window_height, x_cordinate, y_cordinate))
    App(win)
    win.configure(background='white')
    win.mainloop()

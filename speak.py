import text_to_speech
from tkinter import *


class SpeakMain(Toplevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.transient(self.master)
        self.title("Text To Speak")
        self.geometry('1000x300+0+0')
        self.resizable(0, 0)

        Label(self, text="Enter text to speak...", font=("Helvetica", 20)).pack(pady=10)
        self.text = Entry(self, font=("Ubuntu Mono", 30), width=40)
        self.text.pack(pady=10)

        Button(self, text="Speak...", font=("Helvetica", 20), command=self.talk).pack(pady=10)

    def talk(self):
        global text
        text_to_speech.speak(self.text.get(), "en")


if __name__ == '__main__':
    w=Tk()
    SpeakMain()

    w.mainloop()

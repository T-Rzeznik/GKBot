from tkinter import *

from BotSource import get_gpt_response, client

BG_GRAY = "#4B0082"  # Indigo
BG_COLOR = "#2A1C44"  # Deep Purple
TEXT_COLOR = "#EAECEE"
ENTRY_BG_COLOR = "#3B2F5C"  # Slightly lighter purple for entry
BUTTON_BG_COLOR = "#6A0DAD"  # Amethyst
BUTTON_TEXT_COLOR = "#FFFFFF"

FONT = "Arial 14"
FONT_BOLD = "Arial 14 bold"

class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("GKBot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # Head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # Divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # Text widget with scrollbar
        text_frame = Frame(self.window, bg=BG_COLOR)
        text_frame.place(relheight=0.745, relwidth=1, rely=0.08)
        
        self.text_widget = Text(text_frame, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5, wrap=WORD)
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        scrollbar = Scrollbar(text_frame, command=self.text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        # Bottom label for background
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # message entry
        self.msg_entry = Entry(bottom_label, bg = ENTRY_BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely= 0.008, relx= 0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)


        #send button
        send_button = Button(bottom_label, text = "Send", font=FONT_BOLD, width= 20, bg= BUTTON_BG_COLOR, fg=BUTTON_TEXT_COLOR, command= lambda:self._on_enter_pressed(None))
        send_button.place(relx=0.77,rely=0.008, relheight= 0.06, relwidth= 0.22)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._inset_message(msg, "You")

    def _inset_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0,END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"GKBot: {get_gpt_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


if __name__ == "__main__":
    app = ChatApplication()
    app.run()
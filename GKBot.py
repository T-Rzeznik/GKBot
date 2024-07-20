from tkinter import *
from tkinter import ttk  # Import ttk for themed widgets
from tkinter import messagebox
from BotSource import get_gpt_response, client
from PIL import Image, ImageTk

# Define themes
LIGHT_THEME = {
    "BG_COLOR": "#FFFFFF",
    "TEXT_COLOR": "#000000",
    "ENTRY_BG_COLOR": "#F0F0F0",
    "BUTTON_BG_COLOR": "#E0E0E0",
    "BUTTON_TEXT_COLOR": "#000000",
    "BG_GRAY": "#D3D3D3"
}

DARK_THEME = {
    "BG_COLOR": "#2A1C44",
    "TEXT_COLOR": "#EAECEE",
    "ENTRY_BG_COLOR": "#3B2F5C",
    "BUTTON_BG_COLOR": "#6A0DAD",
    "BUTTON_TEXT_COLOR": "#FFFFFF",
    "BG_GRAY": "#4B0082"
}

FONT = "Arial 14"
FONT_BOLD = "Arial 14 bold"
PLACEHOLDER = "Ask anything guitar related!"

class ChatApplication:
    def __init__(self):
        self.window = Tk()
        self.theme = DARK_THEME  # Default theme
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("GKBot")
        self.window.resizable(width=True, height=True)
        self.window.configure(bg=self.theme["BG_COLOR"])

        # Configure grid layout
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Head label
        self.head_label = Label(self.window, bg=self.theme["BG_COLOR"], fg=self.theme["TEXT_COLOR"], text="Welcome to Guitar Knowledge Bot", font=FONT_BOLD, pady=10)
        self.head_label.grid(row=0, column=0, sticky="ew")

        # Settings icon
        settings_image = Image.open("Assets/settings.png")
        settings_image = settings_image.resize((20, 20), Image.LANCZOS)  # Resize the image using LANCZOS
        settings_icon = ImageTk.PhotoImage(settings_image)
        self.settings_button = Button(self.window, image=settings_icon, bg=self.theme["BG_COLOR"], command=self._show_settings_menu)
        self.settings_button.image = settings_icon  # Keep a reference to avoid garbage collection
        self.settings_button.grid(row=0, column=1, sticky="e", padx=10)

        # Divider
        self.line = Label(self.window, bg=self.theme["BG_GRAY"])
        self.line.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Text widget with scrollbar
        text_frame = Frame(self.window, bg=self.theme["BG_COLOR"])
        text_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        self.text_widget = Text(text_frame, bg=self.theme["BG_COLOR"], fg=self.theme["TEXT_COLOR"], font=FONT, wrap=WORD)
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        scrollbar = Scrollbar(text_frame, command=self.text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        # Bottom label for background
        self.bottom_label = Frame(self.window, bg=self.theme["BG_GRAY"])
        self.bottom_label.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # Configure grid layout for bottom_label
        self.bottom_label.grid_columnconfigure(0, weight=1)
        self.bottom_label.grid_columnconfigure(1, weight=0)

        # message entry
        self.msg_entry = Entry(self.bottom_label, bg=self.theme["ENTRY_BG_COLOR"], fg='grey', font=FONT)
        self.msg_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.msg_entry.insert(0, PLACEHOLDER)
        self.msg_entry.bind("<FocusIn>", self._clear_placeholder)
        self.msg_entry.bind("<FocusOut>", self._add_placeholder)
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        self.send_button = ttk.Button(self.bottom_label, text="Send", style="Rounded.TButton", command=lambda: self._on_enter_pressed(None))
        self.send_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    def _clear_placeholder(self, event):
        if self.msg_entry.get() == PLACEHOLDER:
            self.msg_entry.delete(0, END)
            self.msg_entry.configure(fg=self.theme["TEXT_COLOR"])

    def _add_placeholder(self, event):
        if not self.msg_entry.get():
            self.msg_entry.insert(0, PLACEHOLDER)
            self.msg_entry.configure(fg='grey')

    def _show_settings_menu(self):
        menu = Menu(self.window, tearoff=0)
        menu.add_command(label="Light Theme", command=lambda: self._apply_theme(LIGHT_THEME))
        menu.add_command(label="Dark Theme", command=lambda: self._apply_theme(DARK_THEME))
        menu.post(self.window.winfo_pointerx(), self.window.winfo_pointery())

    def _apply_theme(self, theme):
        self.theme = theme
        self.window.configure(bg=self.theme["BG_COLOR"])
        self.head_label.configure(bg=self.theme["BG_COLOR"], fg=self.theme["TEXT_COLOR"])
        self.settings_button.configure(bg=self.theme["BG_COLOR"])
        self.line.configure(bg=self.theme["BG_GRAY"])
        self.text_widget.configure(bg=self.theme["BG_COLOR"], fg=self.theme["TEXT_COLOR"])
        self.bottom_label.configure(bg=self.theme["BG_GRAY"])
        self.msg_entry.configure(bg=self.theme["ENTRY_BG_COLOR"], fg=self.theme["TEXT_COLOR"] if self.msg_entry.get() != PLACEHOLDER else 'grey')
        self.send_button.configure(style="Rounded.TButton")

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        if msg == PLACEHOLDER:
            return
        self._inset_message(msg, "You")

    def _inset_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        self._add_placeholder(None)
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
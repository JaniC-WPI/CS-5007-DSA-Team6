<<<<<<< HEAD:Chatbot_GUI_xyz.py
from tkinter import *
from scrolled_win import ScrolledWindow
import emoji

# emoji resource: https://www.geeksforgeeks.org/python-program-to-print-emojis/
# emoji resource: https://unicode.org/emoji/charts/full-emoji-list.html
emoji_list = [":smiling_face:", ":grinning_face_with_big_eyes:", ":beaming_face_with_smiling_eyes:",
              ":smiling_face_with_halo:", ":winking_face:", ":star-struck:", ":face_blowing_a_kiss:",
              ":face_with_tongue:", ":zany_face:", ":face_with_hand_over_mouth:", ":lying_face:",
              ":pensive_face:", ":face_with_medical_mask:", ":face_with_thermometer:", ":sleepy_face:",
              ":loudly_crying_face:", ":crying_face:", ":pleading_face:", ":nauseated_face:", ":broken_heart:",
              ":weary_face:", ":pouting_face:", ":face_with_steam_from_nose:", ":face_with_symbols_on_mouth:",
              ":angry_face_with_horns:", ":face_screaming_in_fear:", ":confounded_face:", ":disappointed_face:",
              ":persevering_face:", ":anxious_face_with_sweat:"]

def position_to_center(win):
    width = win.winfo_reqwidth()
    height = win.winfo_reqheight()
    right = int(win.winfo_screenwidth() / 2 - width / 2)
    down = int(win.winfo_screenheight() / 2 - height / 2)
    win.geometry("+{}+{}".format(right, down))


class ChatBotGUI:
    def __init__(self):
        self.user_name = ""
        self.conversation_win = None
        self.scrolled_win = None
        self.all_conversations = []
        self.user_input = None
        self.emoji_button = None
        self.bottom_frame = None
        self.input_scrollbar = None
        self.root = Tk()

        position_to_center(win=self.root)

    def start(self):
        welcome_win = Toplevel()
        welcome_win.title("Mental Health ChatBot")
        welcome_win.resizable(width=False, height=False)
        welcome_win.configure(width=300, height=200)

        name_label = Label(welcome_win,
                           text="Please enter your name:",
                           justify=CENTER)
        name_label.place(relx=0.2, rely=0.2)

        name_entry = Entry(welcome_win)
        name_entry.place(relx=0.2, rely=0.3)
        name_entry.focus()

        start_button = Button(welcome_win, text="Start",
                              command=lambda: self.open_chat_win(welcome_win, name_entry.get()))
        start_button.place(relx=0.3, rely=0.45)

        position_to_center(win=welcome_win)

        self.root.mainloop()

    def new_text(self, name, text, align):
        name_widget = Label(self.scrolled_win.scrollwindow, text=name, anchor=align, font=("Bree Serif", 12), foreground="orange")
        name_widget.pack(side=TOP, fill=X)
        self.all_conversations.append(name_widget)

        text_frame = Frame(self.scrolled_win.scrollwindow)
        text_frame.pack(side=TOP, fill=X)
        text_len = int(emoji.demojize(text).count(":") / 2) + len(text) + 1
        text_bg = "white" if name.startswith("ChatBot") else "light gray"
        if text_len < 30:
            text_widget = Text(text_frame, wrap=WORD, background=text_bg, width=text_len, height=1,
                               relief=GROOVE)
        else:
            text_widget = Text(text_frame, wrap=WORD, background=text_bg, width=30, font=10, height=text_len/30,
                               relief=GROOVE)
        text_widget.pack(side=LEFT if align == "nw" else RIGHT)
        text_widget.insert(END, text)
        text_widget.config(state=DISABLED)
        self.all_conversations.append(text_widget)

        self.scrolled_win.canv.update_idletasks()
        self.scrolled_win.canv.yview_moveto("1.0")

    def open_chat_win(self, welcome_win, name):
        self.user_name = name
        welcome_win.destroy()
        self.root.deiconify()
        self.root.title("Mental Health ChatBot")
        self.root.resizable(width=False, height=False)
        self.root.configure(width=400, height=500)

        self.conversation_win = Frame(self.root)
        self.conversation_win.place(relheight=0.90, relwidth=1, rely=0, relx=0)
        self.scrolled_win = ScrolledWindow(parent=self.conversation_win)

        self.new_text(name="ChatBot" + " " * 95,
                      text="Hi " + self.user_name + ", what can I do for you today?",
                      align="nw")

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.place(relheight=0.1, relwidth=1, rely=0.9, relx=0)
        self.emoji_button = Button(self.bottom_frame, command=self.__open_emoji_dialog, text=emoji.emojize(":grinning_face:"),
                                   width=1, height=2)
        self.emoji_button.pack(side=LEFT, fill=X)
        self.user_input = Text(self.bottom_frame, width=60, height=3, wrap=WORD, highlightbackground="gray", highlightcolor="gray", highlightthickness=2)
        self.input_scrollbar = Scrollbar(self.bottom_frame, orient=VERTICAL, command=self.user_input.yview)
        self.input_scrollbar.pack(side=RIGHT, fill=Y)
        self.user_input["yscrollcommand"] = self.input_scrollbar.set
        self.user_input.pack(side=LEFT, fill=X)
        self.user_input.focus()

        #This is where the sent messages are being put!!!!!
        self.user_input.bind("<KeyRelease-Return>", self.__send_message)

        position_to_center(win=self.root)

    def __open_emoji_dialog(self):
        emoji_win = Toplevel()
        emoji_win.title("Emoji")
        emoji_win.resizable(width=False, height=False)
        frame = None
        i = 0
        for e in emoji_list:
            # row of emoji
            if i % 5 == 0:
                frame = Frame(emoji_win)
                frame.pack(side=TOP, fill=Y)
            button = Button(frame, command=lambda estring=e: self.__select_emoji(estring), width=1, height=2, text=emoji.emojize(e))
            button.pack(side=LEFT, fill=X)
            i += 1
        position_to_center(win=emoji_win)

    def __select_emoji(self, emojiString):
        self.user_input.insert(END, emoji.emojize(emojiString))

    #This is what we need to modify!
    def __send_message(self, event):
        # will keep adjustment : add scorllbar in the message area, adjust the size of message area
        # and thing about how to set up "return" as entry or \n
        # if add some emoji what kind do we need? sad, happy, angry, ........?
        message = event.widget.get("1.0", END)
        if not message:
            return
        self.new_text(name=self.user_name, text=message, align="ne")
        self.user_input.delete("1.0", END)
        # Call chatbot to return response.
        self.new_text(name="ChatBot", text="What a good day!", align="nw")


def main():
    gui = ChatBotGUI()
    gui.start()


if __name__ == "__main__":
    main()
=======
from tkinter import *
from scrolled_win import ScrolledWindow
import emoji

# emoji resource: https://www.geeksforgeeks.org/python-program-to-print-emojis/
# emoji resource: https://unicode.org/emoji/charts/full-emoji-list.html
emoji_list = [":smiling_face:", ":grinning_face_with_big_eyes:", ":beaming_face_with_smiling_eyes:",
              ":smiling_face_with_halo:", ":winking_face:", ":star-struck:", ":face_blowing_a_kiss:",
              ":face_with_tongue:", ":zany_face:", ":face_with_hand_over_mouth:", ":lying_face:",
              ":pensive_face:", ":face_with_medical_mask:", ":face_with_thermometer:", ":sleepy_face:",
              ":loudly_crying_face:", ":crying_face:", ":pleading_face:", ":nauseated_face:", ":broken_heart:",
              ":weary_face:", ":pouting_face:", ":face_with_steam_from_nose:", ":face_with_symbols_on_mouth:",
              ":angry_face_with_horns:", ":face_screaming_in_fear:", ":confounded_face:", ":disappointed_face:",
              ":persevering_face:", ":anxious_face_with_sweat:"]

def position_to_center(win):
    width = win.winfo_reqwidth()
    height = win.winfo_reqheight()
    right = int(win.winfo_screenwidth() / 2 - width / 2)
    down = int(win.winfo_screenheight() / 2 - height / 2)
    win.geometry("+{}+{}".format(right, down))


class ChatBotGUI:
    def __init__(self):
        self.user_name = ""
        self.conversation_win = None
        self.scrolled_win = None
        self.all_conversations = []
        self.user_input = None
        self.emoji_button = None
        self.bottom_frame = None
        self.input_scrollbar = None
        self.root = Tk()

        position_to_center(win=self.root)

    def start(self):
        welcome_win = Toplevel()
        welcome_win.title("Mental Health ChatBot")
        welcome_win.resizable(width=False, height=False)
        welcome_win.configure(width=300, height=200)

        name_label = Label(welcome_win,
                           text="Please enter your name:",
                           justify=CENTER)
        name_label.place(relx=0.2, rely=0.2)

        name_entry = Entry(welcome_win)
        name_entry.place(relx=0.2, rely=0.3)
        name_entry.focus()

        start_button = Button(welcome_win, text="Start",
                              command=lambda: self.open_chat_win(welcome_win, name_entry.get()))
        start_button.place(relx=0.3, rely=0.45)

        position_to_center(win=welcome_win)

        self.root.mainloop()

    def new_text(self, name, text, align):
        name_widget = Label(self.scrolled_win.scrollwindow, text=name, anchor=align, font=("Bree Serif", 12), foreground="orange")
        name_widget.pack(side=TOP, fill=X)
        self.all_conversations.append(name_widget)

        text_frame = Frame(self.scrolled_win.scrollwindow)
        text_frame.pack(side=TOP, fill=X)
        text_len = int(emoji.demojize(text).count(":") / 2) + len(text) + 1
        text_bg = "white" if name.startswith("ChatBot") else "light gray"
        if text_len < 30:
            text_widget = Text(text_frame, wrap=WORD, background=text_bg, width=text_len, height=1,
                               relief=GROOVE)
        else:
            text_widget = Text(text_frame, wrap=WORD, background=text_bg, width=30, font=10, height=text_len/30,
                               relief=GROOVE)
        text_widget.pack(side=LEFT if align == "nw" else RIGHT)
        text_widget.insert(END, text)
        text_widget.config(state=DISABLED)
        self.all_conversations.append(text_widget)

        self.scrolled_win.canv.update_idletasks()
        self.scrolled_win.canv.yview_moveto("1.0")

    def open_chat_win(self, welcome_win, name):
        self.user_name = name
        welcome_win.destroy()
        self.root.deiconify()
        self.root.title("Mental Health ChatBot")
        self.root.resizable(width=False, height=False)
        self.root.configure(width=400, height=500)

        self.conversation_win = Frame(self.root)
        self.conversation_win.place(relheight=0.90, relwidth=1, rely=0, relx=0)
        self.scrolled_win = ScrolledWindow(parent=self.conversation_win)

        self.new_text(name="ChatBot" + " " * 95,
                      text="Hi " + self.user_name + ", what can I do for you today?",
                      align="nw")

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.place(relheight=0.1, relwidth=1, rely=0.9, relx=0)
        self.emoji_button = Button(self.bottom_frame, command=self.__open_emoji_dialog, text=emoji.emojize(":grinning_face:"),
                                   width=1, height=2)
        self.emoji_button.pack(side=LEFT, fill=X)
        self.user_input = Text(self.bottom_frame, width=60, height=3, wrap=WORD, highlightbackground="gray", highlightcolor="gray", highlightthickness=2)
        self.input_scrollbar = Scrollbar(self.bottom_frame, orient=VERTICAL, command=self.user_input.yview)
        self.input_scrollbar.pack(side=RIGHT, fill=Y)
        self.user_input["yscrollcommand"] = self.input_scrollbar.set
        self.user_input.pack(side=LEFT, fill=X)
        self.user_input.focus()
        self.user_input.bind("<KeyRelease-Return>", self.__send_message)

        position_to_center(win=self.root)

    def __open_emoji_dialog(self):
        emoji_win = Toplevel()
        emoji_win.title("Emoji")
        emoji_win.resizable(width=False, height=False)
        frame = None
        i = 0
        for e in emoji_list:
            # row of emoji
            if i % 5 == 0:
                frame = Frame(emoji_win)
                frame.pack(side=TOP, fill=Y)
            button = Button(frame, command=lambda estring=e: self.__select_emoji(estring), width=1, height=2, text=emoji.emojize(e))
            button.pack(side=LEFT, fill=X)
            i += 1
        position_to_center(win=emoji_win)

    def __select_emoji(self, emojiString):
        self.user_input.insert(END, emoji.emojize(emojiString))

    def __send_message(self, event):
        # will keep adjustment : add scorllbar in the message area, adjust the size of message area
        # and thing about how to set up "return" as entry or \n
        # if add some emoji what kind do we need? sad, happy, angry, ........?
        message = event.widget.get("1.0", END)
        if not message:
            return
        self.new_text(name=self.user_name, text=message, align="ne")
        self.user_input.delete("1.0", END)
        # Call chatbot to return response.
        self.new_text(name="ChatBot", text="What a good day!", align="nw")


def main():
    gui = ChatBotGUI()
    gui.start()


if __name__ == "__main__":
    main()
>>>>>>> 5d2a6500baae10e46d76ae1af2fd181a46b770a1:GUI/Chatbot_GUI_xyz.py

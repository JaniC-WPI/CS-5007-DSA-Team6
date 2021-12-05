import gui_integration
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
        self.__user_name = ""
        self.__conversation_win = None
        self.__scrolled_win = None
    # the whole conversation between user and ChatBot is saved in a member self.__all_conversations of class ChatBotGUI.
        self.__all_conversations = []
        self.__user_input = None
        self.__emoji_button = None
        self.__bottom_frame = None
        self.__input_scrollbar = None
        self.__root = Tk()

        position_to_center(win=self.__root)

    def start(self):
        welcome_win = Toplevel()
        welcome_win.title("Mental Health ChatBot")
        welcome_win.resizable(width=False, height=False)
        welcome_win.configure(width=300, height=200, highlightbackground = '#2165db', 	highlightcolor = '#2165db', highlightthickness = 5, bg = '#dde3ed')

        name_label = Label(welcome_win,
                           text="Please enter your name:",
                           justify=CENTER, bg = '#dde3ed')
        name_label.place(relx=0.2, rely=0.2)

        name_entry = Entry(welcome_win)
        name_entry.place(relx=0.2, rely=0.3)
        name_entry.focus()

        start_button = Button(welcome_win, text="Start",
                              command=lambda: self.open_chat_win(welcome_win, name_entry.get()))
        start_button.place(relx=0.3, rely=0.45)

        position_to_center(win=welcome_win)

        self.__root.mainloop()

    def new_text(self, name, text, align):
        name_widget = Label(self.__scrolled_win.scrollwindow, text=name, anchor=align, font=("Bree Serif", 12), foreground="orange")
        name_widget.pack(side=TOP, fill=X)
        self.__all_conversations.append(name_widget)
        # create dynamic text_frame to store each dialog. This is a hard work for our project.
        text_frame = Frame(self.__scrolled_win.scrollwindow)
        text_frame.pack(side=TOP, fill=X)
        text_len = int(emoji.demojize(text).count(":") / 2) + len(text) + 1
        text_bg = "#2165db" if name.startswith("ChatBot") else "#04cc65"
        if text_len < 30:
            text_widget = Text(text_frame, wrap=WORD, background=text_bg, width=text_len, height=1, font=("Bree Serif", 12),
                               relief=GROOVE, fg = 'white')
        else:
            text_widget = Text(text_frame, wrap=WORD, background=text_bg, width=30, height=text_len/30, font=("Bree Serif", 12),
                               relief=GROOVE, fg = 'white')
        text_widget.pack(side=LEFT if align == "nw" else RIGHT)
        text_widget.insert(END, text)
        text_widget.config(state=DISABLED)
        self.__all_conversations.append(text_widget)

        self.__scrolled_win.canv.update_idletasks()
        self.__scrolled_win.canv.yview_moveto("1.0")

    def open_chat_win(self, welcome_win, name):
        self.__user_name = name
        welcome_win.destroy()
        self.__root.deiconify()
        self.__root.title("Mental Health ChatBot")
        #Had to change this to true to resize window and see things.
        self.__root.resizable(width=False, height=False)
        self.__root.configure(width=400, height=500)

        self.__conversation_win = Frame(self.__root, highlightbackground = '#2165db', 	highlightcolor = '#2165db', highlightthickness = 5)
        self.__conversation_win.place(relheight=0.90, relwidth=1, rely=0, relx=0)
        self.__scrolled_win = ScrolledWindow(parent=self.__conversation_win)
        # set up 95 empty space for making a nice look new text position
        self.new_text(name="ChatBot" + " " * 78,
                      text="Hi " + self.__user_name + ", what can I do for you today?",
                      align="nw")

        self.__bottom_frame = Frame(self.__root, highlightbackground = '#2165db', 	highlightcolor = '#2165db', highlightthickness = 5)
        self.__bottom_frame.place(relheight=0.1, relwidth=1, rely=0.9, relx=0)
        self.__emoji_button = Button(self.__bottom_frame, command=self.__open_emoji_dialog, text=emoji.emojize(":grinning_face:"),
                                   width=1, height=2)
        self.__emoji_button.pack(side=LEFT, fill=X)
        #Original colors were gray
        self.__user_input = Text(self.__bottom_frame, width=60, height=3, wrap=WORD, highlightbackground="#2165db", highlightcolor="#2165db", highlightthickness=5)
        self.__input_scrollbar = Scrollbar(self.__bottom_frame, orient=VERTICAL, command=self.__user_input.yview)
        self.__input_scrollbar.pack(side=RIGHT, fill=Y)
        self.__user_input["yscrollcommand"] = self.__input_scrollbar.set
        self.__user_input.pack(side=LEFT, fill=X)
        self.__user_input.focus()
        self.__user_input.bind("<KeyRelease-Return>", self.__send_message)

        position_to_center(win=self.__root)

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
        self.__user_input.insert(END, emoji.emojize(emojiString))

    def __send_message(self, event):
        # will keep adjustment : add scorllbar in the message area, adjust the size of message area
        # and thing about how to set up "return" as entry or \n
        # if add some emoji what kind do we need? sad, happy, angry, ........?
        msg = event.widget.get("1.0", END)
        
        stored_response = "May I know where you live? You can give me your zip code just say \"My zip code is\" "
        name_response = gui_integration.name_checker(msg)
        age_response = gui_integration.age_checker(msg)
        
        if msg != '':
            res = gui_integration.chatbot_response(msg)[0]
            self.new_text(name=self.__user_name, text=msg, align="ne")
            self.__user_input.delete("1.0", END)
        # Call chatbot to return response.
            self.new_text(name="ChatBot", text=res, align="nw")
            if res.endswith("I am sorry to hear that, here are some resources and suggestions that might help. Looking things up may take a few minutes. Please give me some time."):
                custom_response = gui_integration.give_url(msg)
                self.new_text(name="ChatBot", text=custom_response, align="nw")

        
        
#             #If the user enters the name then the bot will respond with that name
  
        #     try:
        #     #If the user enters the name then the bot will respond with that name
        #         if res.startswith("Hello"):
        #             gui.insert(END, "Bot: " + res.format(username = name_response) + '\n\n')
        #             #If the user enters the zip code than the zipsearch function is activated and a nearby psychatrist will be google searched and a url is returned
        #             #elif len(msg) == 5 and msg.isdigit() and msg.startswith("0"):
        #         elif msg.startswith("My zip code is"):
        #             msg = msg.strip("My zip code is")
        #             custom_response = zipsearch(msg)
        #             if custom_response != "Thank you for answering.":
        #                 gui.insert(END, custom_response + '\n\n')
        #             else:
        #                 gui.insert(END, custom_response + '\n\n')
        #                 gui.insert(END, "Bot: " + res + '\n\n')
        #                 #All other inputs will be handled here
        #         elif msg == "I decline":
        #             gui.insert(END, "Bot: " + res + '\n\n')
        #             gui.insert(END, "Bot: " + stored_response + '\n\n')
        #         else:
        #             gui.insert(END, "Bot: " + res + '\n\n')
        #         self.__user_input.delete("1.0", END)
                
        #         #This will still run even if the user doesnt activate the custom response so have to put a try/except block here.
        #     except TypeError:
        #         pass
        
        
        
        # gui.config(state=DISABLED)
        # gui.yview(END)
        
    # self.new_text(name=self.user_name, text=message, align="ne")
    # self.__user_input.delete("1.0", END)
        # Call chatbot to return response.
        # self.new_text(name="ChatBot", text="What a good day!", align="nw")


def main():
    gui = ChatBotGUI()
    gui.start()


if __name__ == "__main__":
    main()

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

        self.root.mainloop()

    def new_text(self, name, text, align):
        name_widget = Label(self.scrolled_win.scrollwindow, text=name, anchor=align, font=("Bree Serif", 12), foreground="orange")
        name_widget.pack(side=TOP, fill=X)
        
        #IDK why we are appending all these to a list and doing nothing with it! Doesnt seems to change anything!
        self.all_conversations.append(name_widget)

        text_frame = Frame(self.scrolled_win.scrollwindow)
        text_frame.pack(side=TOP, fill=X)
        text_len = int(emoji.demojize(text).count(":") / 2) + len(text) + 1
        text_bg = "#2165db" if name.startswith("ChatBot") else "#04cc65"
        if text_len < 30:
            text_widget = Text(text_frame, wrap=WORD, background=text_bg, width=text_len, height=1,
                               relief=GROOVE, fg = 'white')
        else:
            text_widget = Text(text_frame, wrap=WORD, background=text_bg, width=30, font=10, height=text_len/30,
                               relief=GROOVE, fg = 'white')
        text_widget.pack(side=LEFT if align == "nw" else RIGHT)
        text_widget.insert(END, text)
        text_widget.config(state=DISABLED)
        
        #IDK why we are appending all these to a list and doing nothing with it! Doesnt seems to change anything!
        self.all_conversations.append(text_widget)

        self.scrolled_win.canv.update_idletasks()
        self.scrolled_win.canv.yview_moveto("1.0")

    def open_chat_win(self, welcome_win, name):
        self.user_name = name
        welcome_win.destroy()
        self.root.deiconify()
        self.root.title("Mental Health ChatBot")
        #Had to change this to true to resize window and see things.
        self.root.resizable(width=False, height=False)
        self.root.configure(width=400, height=500)

        self.conversation_win = Frame(self.root, highlightbackground = '#2165db', 	highlightcolor = '#2165db', highlightthickness = 5)
        self.conversation_win.place(relheight=0.90, relwidth=1, rely=0, relx=0)
        self.scrolled_win = ScrolledWindow(parent=self.conversation_win)
        
        #Change the number value to change where the text box gets located. Changed it from original value of 95 so that longer names can be used and it fits the window
        self.new_text(name="ChatBot" + " " * 78,
                      text="Hi " + self.user_name + ", what can I do for you today?",
                      align="nw")

        self.bottom_frame = Frame(self.root, highlightbackground = '#2165db', 	highlightcolor = '#2165db', highlightthickness = 5)
        self.bottom_frame.place(relheight=0.1, relwidth=1, rely=0.9, relx=0)
        self.emoji_button = Button(self.bottom_frame, command=self.__open_emoji_dialog, text=emoji.emojize(":grinning_face:"),
                                   width=1, height=2)
        self.emoji_button.pack(side=LEFT, fill=X)
        #Original colors were gray
        self.user_input = Text(self.bottom_frame, width=60, height=3, wrap=WORD, highlightbackground="#2165db", highlightcolor="#2165db", highlightthickness=5)
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


""" user_zipcode = []
#None of this has been formally tested yet but it should run
#When the user enters a zip code this function is run. It will double check that the zip code is apart of the state of MA. Need to store zip code moving foreword if it is valid.
def zipsearch(user_input_zipcode):

    #Open up a file containing all the zip codes in Massachusets and copy to a 1D list
    filename = "zipcodes.csv"
    with open(filename, 'r') as csvfile:
        zip_codes = [row.strip().split(",") for row in csvfile]
        flatten_list = list(chain.from_iterable(zip_codes))
    if user_input_zipcode in flatten_list:
        user_zipcode.append(user_input_zipcode)
        return "Thank you for answering."
    else:
        return "Please enter a valid MA zip code"
                    
def give_url(message):
    #We can change the numbers later this is just for the test
    sentiment_analysis_test = 25
    if sentiment_analysis_test > 20:
        try:
                         #Google Search query results as a Python List of URLs
                         query = 'psychiatrists near ' + user_zipcode[0]
                         #Right now it gathers three results from google and puts them into a list. num is the number of results it will find. stop is how many it will put into the list. pause is how many times it will search(I think).
                         search_result_list = list(search(query, tld="co.in", num=3, stop=3, pause=1))
                         #prints out the url if it contains psychology today. This can be changed.
                         for url in search_result_list:
                             if url.startswith('https://www.psychologytoday.com'):
                                 print(url)
                                 return str("Here are a list of psychiatrists in your area: ", url)
        except:
                         return str("Something went wrong with your video search. Please check your internet connection and try again.")
    elif 10 < sentiment_analysis_test <= 20:
        try:
                         #Google Search query results as a Python List of URLs
                         query = 'meditation youtube videos'
                         #Right now it gathers three results from google and puts them into a list. num is the number of results it will find. stop is how many it will put into the list. pause is how many times it will search(I think).
                         search_result_list = list(search(query, tld="co.in", num=3, stop=3, pause=1))
                         #prints out the url if it contains psychology today. This can be changed.
                         for url in search_result_list:
                                 print(url)
                                 return str("Here are some calming Youtube videos for you: ", url)
        except:
                         return str("Something went wrong with your video search. Please check your internet connection and try again.")
    else:
        return "You are fine take a walk and clear your head"

#Need to use this part in the send function 
 elif res.endswith("As well as how long you have been feeling that way"):
                custom_response = give_url(msg)
                ChatLog.insert(END, custom_response + '\n\n') """

def main():
    gui = ChatBotGUI()
    gui.start()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 23:05:39 2021

@author: joshu
"""

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
import pickle
import numpy as np
import chatbot
import re
regex = re.compile('[^a-zA-Z]')
from keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('latest_intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
import emoji
#Creating GUI with tkinter
import tkinter
from tkinter import *
from googlesearch import search
from itertools import chain

# importing the patterns and ignore words from the chatbot.py
documents = chatbot.documents
ignore_words = chatbot.ignore_words

# Creating a list of patterns to be used later to get the response either based on the intents file or the semantic search
doc_lst = []
for i in range(len(documents)):
    doc_lst.append(" ".join(documents[i][0]))


#Tokenizes and lemmatizes the sentences
def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
#Tokenizes pattern and returns an array of the bag of words
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

#Function filters out bot responses below a 25% threshold. Returns most likely
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# Loading the glove vector from the system
def load_glove_model(File):
    # print("Loading Glove Model")
    glove_model = {}
    with open(File, 'r', encoding="utf8") as f:
        for line in f:
            split_line = line.split()
            word = split_line[0]
            embedding = np.array(split_line[1:], dtype=np.float64)
            glove_model[word] = embedding
    # print(f"{len(glove_model)} words loaded!")
    return glove_model
glove_vectors = load_glove_model("glove.6B.50d.txt")

# creating the word vectors from the input
def get_sentence_vector(sentence):
    sent_array = []
    for word in sentence.split():
        temp = word.strip()
        # print("Temp", temp)
        temp = regex.sub('', temp)
        # print("Temp", temp)
        temp = temp.lower()
        # print("Temp", temp)
        sent_array.append(glove_vectors[temp])
        # print("sent_array", sent_array)
    return(np.mean(sent_array, axis=0))

# Semantic analysis
def semantic_search(user_input, intents_json):    
    sim_score = []
    for i in range(len(documents)):
        # print(corpus)
        doc1 = user_input
        # print(doc1)
        doc1_vector = get_sentence_vector(doc1)
        doc2 = [doc for doc in documents[i][0] if doc not in ignore_words]
        # print(doc2)
        doc2 = " ".join(doc2)
        # print(doc2)
        doc2_vector = get_sentence_vector(doc2)    
        sim_lst = cosine_similarity([doc1_vector, doc2_vector])
        sim_score.append(sim_lst[1][0])
    tag = documents[sim_score.index(max(sim_score))][1]
    print(tag)
    # print(max(sim_score))
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result, tag

# Assess the severity of mental illness and provides response accordingly
def sentiment_analysis(user_input):
    scores = sid.polarity_scores(user_input)
    if scores['compound'] <-0.2:
        return 'Psychiatric consultation'
    elif (-0.2 <= scores['compound'] <= 0.2):
        return 'send youtube video'
    else:
        return 'you are ok'


#Based off intents file tags generates a response
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    print(tag)
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result, tag


#Handles the bots responses based off the input and intents file and semantic search
def chatbot_response(msg):
    print("Message is", msg)
# print(doc_lst)
    if msg in doc_lst:
        print(msg in doc_lst)
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        if res1[1] in ('Depression', 'psychosis'):
            res3 = sentiment_analysis(msg)
        return res1[0]
    else:
        print(msg in doc_lst)
        res2 = semantic_search(msg, intents)
        if res2[1] in ('Depression', 'psychosis'):
            res4 = sentiment_analysis(msg)
        return res2[0]

#When the user enters a zip code this function is run. It will double check that the zip code is apart of the state of MA. Need to store zip code moving foreword if it is valid.
def zipsearch(user_input_zipcode):

    #Open up a file containing all the zip codes in Massachusets and copy to a 1D list
    filename = "zipcodes.csv"
    with open(filename, 'r') as csvfile:
        zip_codes = [row.strip().split(",") for row in csvfile]
        flatten_list = list(chain.from_iterable(zip_codes))
    if user_input_zipcode in flatten_list:
        return "Thank you for answering."
    else:
        return "Please enter a valid MA zip code"
                    
# =============================================================================
#             Need to reconfigure this later to look up google search based on zip code       
 #Try/except block is meant to handle any error that comes with being unable to connect to the internet
#                     try:
#                         #Google Search query results as a Python List of URLs
#                         query = 'psychiatrists near ' + user_input_zipcode
#                         #Right now it gathers three results from google and puts them into a list. num is the number of results it will find. stop is how many it will put into the list. pause is how many times it will search(I think).
#                         search_result_list = list(search(query, tld="co.in", num=3, stop=3, pause=1))
#                         #prints out the url if it contains psychology today. This can be changed.
#                         for url in search_result_list:
#                             if url.startswith('https://www.psychologytoday.com'):
#                                 print(url)
#                                 return str(url)
#                     except:
#                         return str("Something went wrong with the search. Please check your internet connection and try again.")
# =============================================================================
                    

#If the user enters "My name is " this function will run 
def name_checker(check_msg):
    if check_msg.startswith("My name is"):
        return check_msg.replace("My name is ", "")

def age_checker(check_msg):
    if check_msg.endswith(" years old"):
        return check_msg.replace(" years old", "")

#Function handles the text entered into the text box and gives responses based on the input.     
def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    
    stored_response = "May I know where you live? You can give me your zip code just say \"My zip code is\" "
    name_response = name_checker(msg)
    age_response = age_checker(msg)
    
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
        #We will need to consider these two lines when responding. 
        #Could modify the response from the JSON file here. This would enable us to add personal name and other details that the user enters.
        res = chatbot_response(msg)
        try:
            #If the user enters the name then the bot will respond with that name
            if res.startswith("Hello"):
                ChatLog.insert(END, "Bot: " + res.format(username = name_response) + '\n\n')
            #If the user enters the zip code than the zipsearch function is activated and a nearby psychatrist will be google searched and a url is returned
            #elif len(msg) == 5 and msg.isdigit() and msg.startswith("0"):
            elif msg.startswith("My zip code is"):
                msg = msg.strip("My zip code is")
                custom_response = zipsearch(msg)
                if custom_response != "Thank you for answering.":
                    ChatLog.insert(END, custom_response + '\n\n')
                else:
                    ChatLog.insert(END, custom_response + '\n\n')
                    ChatLog.insert(END, "Bot: " + res + '\n\n')
            #All other inputs will be handled here
            elif msg == "I decline":
                ChatLog.insert(END, "Bot: " + res + '\n\n')
                ChatLog.insert(END, "Bot: " + stored_response + '\n\n')
            else:
                ChatLog.insert(END, "Bot: " + res + '\n\n')
                
                #This will still run even if the user doesnt activate the custom response so have to put a try/except block here.
        except TypeError:
            pass
        
        
        
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

    
base = Tk()
base.title("Hello")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")


#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

base.mainloop()

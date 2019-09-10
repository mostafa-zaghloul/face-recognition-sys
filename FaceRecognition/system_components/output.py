from utils.number_to_string import *
import tkinter as tk
#import win32com.client as wincl

#windows10_voice_interface = wincl.Dispatch("SAPI.SpVoice")

def output(identities,master):
    unknown = 0
    known = 0
    known_arr = []
    total_message = ""
    #print(str(len(identities)))
    if(len(identities) > 0):
        if(len(identities) < 11):
            ids=to_str(len(identities))
            #print(ids + " detected")
            total_message = total_message + ids + " detected "
        else:
            #print(str(len(identities)) + " detected")
            total_message = total_message + str(len(identities)) + " detected, "
        for person in identities:
            if(person =="unknown"):
                unknown=+1
            else:
                known=+1
                known_arr.append(person)
        if(known < 11):
            k=to_str(known)
            #print(k + " you know")
            total_message = total_message + k + " you know "
        else:
            #print(str(known) + " people you know")
            total_message = total_message + str(known) + " you know "
        if(known > 0):
            #print("say hi to ")
            total_message = total_message + ", say hi to "
            for i in known_arr:
                #print(i + " ")
                total_message = total_message + i + " "
    else:
        #print("NO ONE DETECTED")
        total_message = "No One Dtected"

    #print(total_message)
    label = tk.Label(master, text=total_message, bg="white", fg="red")
    label.pack()
    #windows10_voice_interface.Speak(total_message)
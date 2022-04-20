from tkinter import filedialog
from tkinter import *
import tkinter as tk
import numpy as np
import requests
import wget

url_ygoprodeck = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

folder=None
ydk=None

def get_folder():
    global folder
    folder=filedialog.askdirectory()


def get_ydk():
    global ydk
    ydk=filedialog.askopenfilename()

def remove_trailing_func(x):
    try:
        return int(x.rstrip())
    except(ValueError):
        return np.nan

remove_trailing= lambda x: remove_trailing_func(x)

def read_ydk(ydk):
    lines = [line.rstrip() for line in open(ydk)]
    for l in lines:
        if '!' in l: lines=list(filter((l).__ne__,lines))
        elif '#' in l: lines=list(filter((l).__ne__,lines))
    lines_unique = np.array(np.unique(np.array(lines)))
    return lines_unique


def get_cards(cards_lines, download_location):
    cards_to_download = []
    for c in cards_lines:
        r = requests.get(url=url_ygoprodeck, params={'id': c})
        cards_to_download.append(r.json()['data'][0]['card_images'][0]['image_url'])

    for d in cards_to_download:
        wget.download(d, download_location)


def turn_ydk_to_images():
    get_cards(read_ydk(ydk),folder)

root = tk.Tk()
root.title('Bigmens Yugioh Card Mass Downloader')

def exit_program():
    root.destroy()


canvas1 = tk.Canvas(root, width=200, height=150)
label = Label(canvas1, text= "Select a Folder to download the images, then select a ydk file to download every image in that deck", font= ('Helvetica 14 bold'))
label.pack(pady=1)

canvas1.pack(side='top')

button1=tk.Button(canvas1, text= "Select Folder to download the Images to", command= get_folder).pack(side=TOP)
button2=tk.Button(canvas1,text="Select YDK file to pull cards from", command=get_ydk).pack(side=TOP)
button3=tk.Button(canvas1,text="Start!",command=turn_ydk_to_images).pack(side=TOP)




root.mainloop()

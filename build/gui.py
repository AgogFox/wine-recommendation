import numpy as np 
from numpy import dot
from numpy.linalg import norm
import pandas as pd 
import copy
import seaborn as sn
import matplotlib.pyplot as plt
from pandastable import Table, TableModel

#import csv
df = pd.read_csv('.\cleansingWine.csv').drop('Unnamed: 0', axis=1)

#remove var name
for i in range(1,6):
    i = str(i)
    df['sweet'] = df['sweet'].replace(('SWEET'+i),i)
    df['acidity'] = df['acidity'].replace(('ACIDITY'+i),i)
    df['body'] = df['body'].replace(('BODY'+i),i)
    df['tannin'] = df['tannin'].replace(('TANNIN'+i),i)
df = df.fillna(0)

#if range convert to average
abv = []
for i in range(len(df)):
    try:
        x,y = df['abv'][i].split('~')
        abv.append((float(x)+float(y))/2)
    except:
        abv.append(df['abv'][i])
df.abv = abv

degree = []
for i in range(len(df)):
    try:
        x,y = df['degree'][i].split('~')
        degree.append((float(x)+float(y))/2)
    except:
        degree.append(df['degree'][i])
        continue
df.degree = degree

#convert won to thb
thb = []
for i in df.price:
    thb.append(i*0.027)
df.price = thb
print(df[['price', 'abv', 'degree']])

t = copy.deepcopy(df) #copy of display

#map variety to number
s = set()
for i in df.columns[8:20]:
    for j in list(df[i].unique()):
        if j == 0:
            j = '0'
        s.add(j)

v_arr = list(s)
v_arr.sort()
v_dic = {i : v_arr.index(i) for i in v_arr}

#change variety to number in dataframe
for i in df.columns[8:20]:
    arr = []
    for j in df[i]:
        if j == 0:
            j = '0'
        if j == None:
            arr.append(0)
        else:
            arr.append(v_dic[j])
    df[i] = arr


#map nation name to number
s = set()
for j in list(df['nation'].unique()):
    if j == 0:
        j = '0'
    s.add(j)
n_arr = list(s)
n_arr.sort()
n_dic = {i : n_arr.index(i) for i in n_arr}

#change nation to number in dataframe
arr = []
for i in df['nation']:
    if i == 0:
        i = '0'
    if i == None:
        arr.append(0)
    else:
        arr.append(n_dic[i])
df['nation'] = arr

#change type object to float for calculation
tmp = df[['nation', 'varieties1','varieties2', 'varieties3', 'varieties4', 'varieties5', 'varieties6', 'varieties7', 
        'varieties8', 'varieties9', 'varieties10', 'varieties11', 'varieties12','abv', 'degree', 'sweet', 'acidity', 'body', 'tannin']]
tmp['abv'] = tmp['abv'].astype('float64')
tmp['degree'] = tmp['degree'].astype('float64')
tmp['sweet'] = tmp['sweet'].astype('int64')
tmp['acidity'] = tmp['acidity'].astype('int64')
tmp['body'] = tmp['body'].astype('int64')
tmp['tannin'] = tmp['tannin'].astype('int64')

#********************************^^^data_cleaning^^^***********************************


def user_in(arr):
    user_input = []
    try:
        tmp_inp = n_dic[arr[0]]
    except:
        tmp_inp = 0
    user_input.append(tmp_inp)
    try:
        tmp_inp = v_dic[arr[1]]
    except:
        tmp_inp = 0
    tmp_inp = [tmp_inp] * 12
    user_input.extend(tmp_inp)

    tmp_inp = int(arr[2])
    user_input.append(tmp_inp)

    tmp_inp = int(arr[3])
    user_input.append(tmp_inp)

    tmp_inp = int(arr[4])
    user_input.append(tmp_inp)

    tmp_inp = int(arr[5])
    user_input.append(tmp_inp)

    tmp_inp = int(arr[6])
    user_input.append(tmp_inp)

    tmp_inp = int(arr[7])
    user_input.append(tmp_inp)

    user_input = np.array([int(x) for x in user_input]) #convert to vector
    return user_input



def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))

def process(user_input): #check each wine against user input using cosine similarity
    sim = []
    for i in range(0, len(tmp)):
        sim.append(cos_sim(user_input, tmp.iloc[i].values))

    coss = pd.DataFrame({'id' : df['id'][0:].tolist(), 'sim' : sim})

    x = pd.concat([t.reset_index().drop('index', axis=1).drop('id', axis=1), coss], axis=1).sort_values(by=['sim'], ascending=False).head(10)
    y = pd.concat([tmp, coss], axis=1).sort_values(by=['sim'], ascending=False).head(10) #nation and variety will be number
    
    return x, y

# ------------------------------------------------process----------------------------------------------------------------

from pathlib import Path
from tkinter import *
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage ,ttk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"..\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("900x600")
window.configure(bg = "#FFFFFF")

#-----------------------------------------change page----------------------------------------
def change_to_work():
    a = []
    a.append(in1.get())
    a.append(in2.get())
    a.append(in3.get())
    a.append(in4.get())
    a.append(in5.get())
    a.append(in6.get())
    a.append(in7.get())
    a.append(in8.get())
    eiei, eiei2 = process(user_in(a))

    work_frame.pack(fill='both',expand=True)
    #for table
    table = Table(work_frame, dataframe=eiei)
    table.show()
    #for heatmap
    heat = eiei2[['nation', 'varieties1','varieties2', 'varieties3', 'varieties4', 'varieties5', 'varieties6', 'varieties7', 
            'varieties8', 'varieties9', 'varieties10', 'varieties11', 'varieties12', 'abv', 'degree', 'sweet', 'acidity', 'body', 'tannin']]

    heat = heat.corr()
    sn.heatmap(heat)
    plt.show()

def change_to_quiz():
    quiz_frame.pack(fill='both', expand=1)
    work_frame.forget()

#-------------------------end change page--------------------------------------

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    450.0,
    124.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    454.0,
    432.4192352294922,
    image=image_image_2
)

#Tannin
in8 = Spinbox(window, from_=0, to=5)
in8.place(x=415.0,
    y=547.0,)
# canvas.create_rectangle(
#     415.0,
#     541.0,
#     503.0,
#     573.0,
#     fill="#D9D9D9",
#     outline="")

#white block
canvas.create_rectangle(
    113.0,
    85.0,
    788.0,
    341.0,
    fill="#FFFFFF",
    outline="")

#red rectangle block
canvas.create_rectangle(
    112.0,
    85.0,
    393.0,
    341.0,
    fill="#B62831",
    outline="")

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    383.0,
    213.0,
    image=image_image_3
)

canvas.create_text(
    145.0,
    125.0,
    anchor="nw",
    text="WINE",
    fill="#FFFFFF",
    font=("JockeyOne Regular", 70 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    88.0,
    33.0,
    image=image_image_4
)

#block to insert image
canvas.create_rectangle(
    437.0,
    102.0,
    756.0,
    275.0,
    fill="#D9D9D9",
    outline="")

#nation
in1_var = StringVar()
in1 = ttk.Combobox(window, textvariable=in1_var)

in1['values'] = list(n_dic.keys())

def on_select(event):
    selected_option = in1.get()
    selected_value = n_dic.get(selected_option, "N/A")
    print(f"Selected Option: {selected_option}, Selected Value: {selected_value}")

in1.bind("<<ComboboxSelected>>", on_select)
in1.place(x=117.0,y=392.0)

# canvas.create_rectangle(
#     117.0,
#     388.0,
#     292.0,
#     420.0,
#     fill="#D9D9D9",
#     outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=718.0,
    y=297.0,
    width=22.0,
    height=24.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=454.0,
    y=297.0,
    width=22.0,
    height=24.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    73.0,
    403.0,
    image=image_image_5
)

#degree
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    499.5,
    458.0,
    image=entry_image_2
)
in4 = Entry(
    window,
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
in4.place(
    x=428.0,
    y=442.0,
    width=143.0,
    height=30.0
)
image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    359.0,
    457.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    358.0,
    402.0,
    image=image_image_7
)

#varity
entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    499.5,
    404.0,
    image=entry_image_3
)
in2 = Entry(
    window,
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
in2.place(
    x=428.0,
    y=388.0,
    width=143.0,
    height=30.0
)
# canvas.create_rectangle(
#     412.0,
#     388.0,
#     587.0,
#     420.0,
#     fill="#D9D9D9",
#     outline="")

#ABV
entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    204.5,
    458.0,
    image=entry_image_4
)
in3 = Entry(
    window
    ,bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
in3.place(
    x=133.0,
    y=442.0,
    width=143.0,
    height=30.0
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    74.0,
    457.0,
    image=image_image_8
)

#sweet
in5 = Spinbox(window, from_=0, to=5)
in5.place(x=117.0,y=505.0) 
# canvas.create_rectangle(
#     117.0,
#     496.0,
#     205.0,
#     528.0,
#     fill="#D9D9D9",
#     outline="")

#acidity
in6 = Spinbox(window, from_=0, to=5)
in6.place(x=417.0,y=505.0) 


#body
in7 = Spinbox(window, from_=0, to=5)
in7.place(x=117.0,y=548.0) 


image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    74.0,
    513.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    74.0,
    554.0,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    360.0,
    555.0,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    361.0,
    513.0,
    image=image_image_12
)

canvas.create_text(
    156.0,
    206.0,
    anchor="nw",
    text="Recommendation",
    fill="#FFFFFF",
    font=("Mitr Regular", 20 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=521.0,
    y=28.0,
    width=25.001922607421875,
    height=19.442276000976562
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=664.0,
    y=28.0,
    width=24.21875,
    height=24.21875
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command= change_to_work,
    relief="flat"
)
button_3.place(
    x=701.0,
    y=525.0,
    width=147.0,
    height=46.0
)
button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=824.0,
    y=31.0,
    width=19.0,
    height=19.0
)

quiz_frame = Frame(window)
work_frame = Frame(window)
window.resizable(False, False)
window.mainloop()

#Cabernet Sauvignon
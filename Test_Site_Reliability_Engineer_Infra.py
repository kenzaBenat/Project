import requests
import json
from tkinter import *
from tkinter import ttk


# Function that return all the episodes and their title bases on the series name
def search_serie(name):

    url2 = 'http://api.tvmaze.com/search/shows?q='+name

    df2 = requests.get(url2)
    df_text2 = df2.text
    data = json.loads(df_text2)


    df = requests.get(url2)
    df_text = df.text
    data = json.loads(df_text)
    id = data[0]['show']['id']
    print(id)

    url = 'https://api.tvmaze.com/shows/' + str(id) + '/episodes'
    df = requests.get(url)
    df_text = df.text
    data2 = json.loads(df_text)

    return data2

# Function that opens a second window that contains all the episodes
def submit():
    window.withdraw()
    window2 = Tk()
    window2.title('Result Search')
    window2.geometry("700x600")

    scrollbar = Scrollbar(window2)
    scrollbar.pack(side=RIGHT, fill=Y)

    serie_name = entry.get()
    data = search_serie(serie_name)
    list = []
    treeview = ttk.Treeview(window2, style="mystyle.Treeview", height=len(data),yscrollcommand=scrollbar.set)
    treeview["columns"] = ["Season", "Episode", "Name"]
    treeview["show"] = "headings"
    treeview.heading("Season", text="Season")
    treeview.heading("Episode", text="Episode")
    treeview.heading("Name", text="Name")

    for line in data:
        list.append((str(line['season']), str(line['number']), str(line['name'])))

    index = iid = 0

    x = 'odd'
    for row in list:
        treeview.insert("", index, iid, values=row, tags=(x,))
        index = iid = index + 1
        if index == 1: x = 'even';
        if index == 2: x = 'odd';

    treeview.column("Season", anchor="center")
    treeview.column("Episode", anchor="center")
    treeview.column("Name", anchor="center")

    treeview.tag_configure('odd', background='#F1F2F6')
    treeview.tag_configure('even', background='#DADBDD')
    treeview.pack(padx=10, fill=BOTH)
    scrollbar.config(command=treeview.yview)

    window2.mainloop()

# First window to write down the name of the serie we wish to search
window = Tk()
window.title("Search TV series")
window.geometry("700x200")
label = Label(window, text="Search a TV show :")
label.pack()
entry = Entry(window)
entry.place(x=265, y=30)
button = Button(window, text="ok", command=submit)
button.place(x=405, y=25)

window.mainloop()




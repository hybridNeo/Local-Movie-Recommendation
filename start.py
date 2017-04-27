import sys
import os
import omdb  # https://pypi.python.org/pypi/omdb#downloads
import glob
import operator
import string
import re

import tkinter
from tkinter.filedialog import *
from tkinter import filedialog


reserved_audio = ['5.1', '7.1', '5 1', '7 1', 'DUAL AUDIO', 'DUAL-AUDIO', 'MULTI-CHANNEL', 'Ita-Eng']
reserved_video = ['2160p', '4K', '1080p', '720p', '480p', '360p', 'HD', 'FULL HD', 'FULLHD']
reserved_codecs = ['x264', 'CH', 'X264', 'HEVC']
reserved_medium = ['WEB-DL', 'BrRip', 'Rip', 'DVDRip', 'XviD', 'BLURAY']
reserved_keywords = ['EXTENDED', 'REMASTERED', 'DIRECTORS', 'UNRATED', 'AlTERNATE']
reserved_other = ['[]', '-aXXo']


def remove(substr, str):
    index = 0
    length = len(substr)
    while string.find(str, substr) != -1:
        index = string.find(str, substr)
        str = str[0:index] + str[index+length:]
    return str


def search(list):
    dic = {}
    err_cnt = 0
    for i in list:
        try:
            obj = omdb.title(i)
            if(obj != []):
                dic[i] = obj.imdb_rating
        except:
            err_cnt+=1
    return (dic)


def clean(raw_list):
    movies = []
    reserved_words = reserved_audio + reserved_video + reserved_codecs + reserved_medium + \
                     reserved_keywords + reserved_other

    for full_movie_name in raw_list:
        clean_movie_name = full_movie_name.replace('.', ' ')  # "Shift.HEVC.UNRATED" becomes "Shift HEVC UNRATED"

        for reserved_word in reserved_words:
            if reserved_word in clean_movie_name:
                name_movie_after_erasure = clean_movie_name.replace(reserved_word, "")
                clean_movie_name = name_movie_after_erasure

        # Regex
        clean_movie_name = re.sub(r'^www.\/\/.*[\r\n]*', '', clean_movie_name, flags=re.MULTILINE)
        clean_movie_name = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', clean_movie_name, flags=re.MULTILINE)
        movies.append(clean_movie_name)

    return movies

def Convert_Coordinates_To_String(x_coordinate, y_coordinate):
    coordinates_as_string = "+" + str(x_coordinate) + "+" + str(y_coordinate)
    return coordinates_as_string


def main():
    omdb.set_default('tomatoes', True)

    ''' TOP WINDOW '''
    top_window = tkinter.Tk()  # Main window of application.
    top_window.withdraw()  # Hide main window. Call deiconify() to make it visible again.

    x_coordinate = 0
    y_coordinate = 100
    coordinates_as_string = Convert_Coordinates_To_String(x_coordinate, y_coordinate)  # Looks like "+500+100"
    top_window.geometry(coordinates_as_string)
    ''' '''

    ''' PUT LABEL ON TO THE OTHER WINDOW '''
    additional_window = Toplevel()
    coordinates_as_string = Convert_Coordinates_To_String(x_coordinate, y_coordinate - 25)
    additional_window.geometry(coordinates_as_string)

    label = Label(additional_window, text = "Please choose a folder with movies.", relief = RAISED, padx = 25)
    label_options = {}
    label_options['foreground'] = "blue"
    label_options['background'] = "white"
    label.configure(**label_options)
    label.pack()  # This geometry manager organizes widgets in blocks before placing them in the parent widget.
    ''' '''

    browser_options = {}
    browser_options['initialdir'] = "C:\\"  # Specifies which directory should be displayed when the dialog pops up.
    browser_options['title'] = "Select folder with movies"

    dirname = tkinter.filedialog.askdirectory(**browser_options)

    #top_window.destroy()
    #top_window.mainloop()  # Unneceasary for now - when user choses folder we must switch off GUI for the time of searching.


    if(dirname == ""):
        dirname = os.path.dirname(os.path.realpath(__file__))
    if(len(sys.argv) ==  2):
        dirname = sys.argv[1]

    raw_movies = os.listdir(dirname)


    print('Cleaning.....')
    l = clean(raw_movies)

    print('Retrieving Info... \n \n')
    info = search(l)

    sorted_x = sorted(info.items(), key=operator.itemgetter(1))
    sorted_x = sorted_x[::-1]
    found = 0

    for i in sorted_x:
        print(i[0] + ' --------------- ' + str(i[1]))
        found = found + 1
    # search = omdb.title('The Matrix')
    # print(search.imdb_rating)
    # print(search.tomato_rating)
    if found == 0:
        print("No movies were found\nPlease check directory or file names")

if __name__ == '__main__':
    main()

    '''TO DO: 
    1. After program gets all ratings, show it in new GUI window.
    2. Make it multithreading, so 1 thread shows GUI in mainloop() and second thread works on everything else.
    3. Allow user to select multiple folders. (tkFileDialog has "multiple" option)
    4. Get size of File Dialog Windows in Windows and make label centered above this dialog. Links below.
    '''

    # screen_width = top_window.winfo_screenwidth()
    # screen_height = top_window.winfo_screenheight()
    # top_window.geometry('%dx%d+%d+%d' % (screen_width, screen_height, x_coordinate, y_coordinate))


''' 
The package Tkinter has been renamed to tkinter in Python 3, as well as other modules related to it. 
Here are the name changes:

Tkinter → tkinter
tkMessageBox → tkinter.messagebox
tkColorChooser → tkinter.colorchooser
tkFileDialog → tkinter.filedialog
tkCommonDialog → tkinter.commondialog
tkSimpleDialog → tkinter.simpledialog
tkFont → tkinter.font
Tkdnd → tkinter.dnd
ScrolledText → tkinter.scrolledtext
Tix → tkinter.tix
ttk → tkinter.ttk
'''

''' 
Causing a widget to appear requires that you position it using with what Tkinter calls "geometry managers". 
The three managers are grid, pack and place.
'''
# label.grid(row = 50, column = 1000)  # This geometry manager organizes widgets in a table-like structure in the parent widget.
# label.place(x = 1)

 # https://bytes.com/topic/python/answers/908537-can-window-size-tffiledialog-changed
 # http://stackoverflow.com/questions/21558028/how-to-change-window-size-of-tkfiledialog-askdirectory




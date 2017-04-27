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


def get_movies_info(movie_list):
    ratings = {}
    box_office = {}
    release_date = {}
    length = {}
    votes_number = {}
    full_title = {}

    err_cnt = 0
    for movie_name in movie_list:
        try:
            movie = omdb.title(movie_name)
            if movie:
                ratings[movie_name] = movie.imdb_rating
                box_office[movie_name] = movie.box_office
                release_date[movie_name] = movie.released
                length[movie_name] = movie.runtime
                votes_number[movie_name] = movie.imdb_votes
                full_title[movie_name] = movie.title
        except:
            err_cnt += 1

    return ratings


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


class GUI_Manager:

    def convert_coordinates_to_string(self, x=0, y=0):
        coordinates_as_string = "+" + str(self._x_coordinate + x) + "+" + str(self._y_coordinate + y)
        return coordinates_as_string

    def set_root_window(self):
        self.top_window.withdraw()  # Hide main window. Call deiconify() to make it visible again.
        self.top_window.geometry(self.convert_coordinates_to_string())

    def set_additional_window(self):
        # Additional window is created so that label can bind to it. It needs to be a little bit higher then
        # opening folder Dialog, so the text on label is visible.
        above_file_dialog_coordinate = - 25
        self.additional_window.geometry(self.convert_coordinates_to_string(y=above_file_dialog_coordinate))

    def set_label_options(self):
        self.label_options['foreground'] = "blue"
        self.label_options['background'] = "white"

    def set_browser_options(self):
        self.browser_options['initialdir'] = "C:\\"  # Specifies which directory should be displayed when the dialog pops up.
        self.browser_options['title'] = "Select folder with movies"

    def set_label(self):
        self.label.configure(**self.label_options)
        self.label.pack()  # This geometry manager organizes widgets in blocks before placing them in the parent widget.

    def open_folder_browser(self):
        return tkinter.filedialog.askdirectory(**self.browser_options)

    def get_folder_path(self):
        return self.directory_path

    def __init__(self):
        self._x_coordinate = 0
        self._y_coordinate = 100

        self.top_window = tkinter.Tk()
        self.additional_window = Toplevel()
        self.label = Label(self.additional_window, text = "Please choose a folder with movies.",
                           relief = RAISED, padx = 25)

        self.label_options = {}
        self.browser_options = {}

        self.set_root_window()
        self.set_additional_window()

        self.set_label_options()
        self.set_label()

        self.set_browser_options()

        self.directory_path = self.open_folder_browser()


def main():
    omdb.set_default('tomatoes', True)

    manager = GUI_Manager()
    directory_path = manager.get_folder_path()

    if directory_path == "":
        directory_path = os.path.dirname(os.path.realpath(__file__))
    if len(sys.argv) == 2:
        directory_path = sys.argv[1]

    raw_movies = os.listdir(directory_path)

    print('Cleaning.....')
    movie_list = clean(raw_movies)

    print('Retrieving Info... \n \n')
    movie_informations = get_movies_info(movie_list)

    movie_informations = sorted(movie_informations.items(), key=operator.itemgetter(1), reverse=True)

    for movie_rating in movie_informations:
        print(movie_rating[0] + ' --------------- ' + str(movie_rating[1]))

    # get_movies_info = omdb.title('The Matrix')
    # print(get_movies_info.imdb_rating)
    # print(get_movies_info.tomato_rating)

    if not movie_informations:
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




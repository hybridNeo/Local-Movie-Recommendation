import sys
import os
import omdb  # https://pypi.python.org/pypi/omdb#downloads
import glob
import operator
import string
import re

import tkinter
import tkinter.messagebox
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
    movies_not_recognized = []

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
            else:
                movies_not_recognized.append(movie_name)
        except:
            err_cnt += 1

    movie_informations = {'Ratings': ratings, 'Box_office': box_office, 'Release_date': release_date, 'Length': length,
                           'Votes_number': votes_number, 'Full_title': full_title, 'Not_recognized': movies_not_recognized}
    return movie_informations


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

    @staticmethod
    def convert_coordinates_to_string(x=0, y=0):
        x = int(x)
        y = int(y)
        coordinates_as_string = "+" + str(x) + "+" + str(y)  # Looks like '+500+100'
        return coordinates_as_string

    def set_root_window(self):
        self.top_window.withdraw()  # Hide main window. Call deiconify() to make it visible again.
        self.top_window.geometry(self.convert_coordinates_to_string(x=self._x_coordinate, y=self._y_coordinate))

    def set_browser_options(self):
        self.browser_options['initialdir'] = "C:\\"  # Specifies which directory should be displayed when the dialog pops up.
        self.browser_options['title'] = "Select folder with movies"

    def open_folder_browser(self):
        directory_path = tkinter.filedialog.askdirectory(**self.browser_options)
        return directory_path

    def get_folder_path(self):
        self.directory_path = self.open_folder_browser()
        return self.directory_path

    def show_ratings(self, movies_information):
        rating_label = Label(self.top_window, text="Ratings")
        rating_label.grid(row = 0, column = self._column)

        rating_list = Listbox(self.top_window)
        rating_list.grid(row = 1, column = self._column)

        self._column += 1

        movies_ratings = sorted(movies_information['Ratings'].items(), key=operator.itemgetter(1), reverse=True)
        for movie_rating in movies_ratings:
            rating_list.insert(END, str(movie_rating[0] + ': ' + str(movie_rating[1])))

    def show_box_office(self, movies_information):
        box_office_label = Label(self.top_window, text="Box Office")
        box_office_label.grid(row = 0, column = self._column)

        box_office_list = Listbox(self.top_window)
        box_office_list.grid(row = 1, column = self._column)

        self._column += 1

        movies_box_office = sorted(movies_information['Box_office'].items(), key=operator.itemgetter(1), reverse=True)
        for movie_money in movies_box_office:
            box_office_list.insert(END, str(movie_money[0] + ': ' + str(movie_money[1])))

    def show_length(self, movies_information):
        length_label = Label(self.top_window, text="Length")
        length_label.grid(row = 0, column = self._column)

        length_list = Listbox(self.top_window)
        length_list.grid(row = 1, column = self._column)

        self._column += 1

        # Strip string from length, ie: 88 min  -> 88
        for movie_name, duration in movies_information['Length'].items():
            length_purified = int(re.match(r'\d+', duration).group())
            movies_information['Length'][movie_name] = length_purified

        movies_length = sorted(movies_information['Length'].items(), key=operator.itemgetter(1), reverse=True)

        for movie_length in movies_length:
            print((movie_length[1]))
            length_list.insert(END, str(movie_length[0] + ': ' + str(movie_length[1]) + " min."))

    def show_release_date(self, movies_information):
        release_date_label = Label(self.top_window, text="Release date")
        release_date_label.grid(row = 0, column = self._column)

        release_date_list = Listbox(self.top_window)
        release_date_list.grid(row = 1, column = self._column)

        self._column += 1

        movies_release_date = sorted(movies_information['Release_date'].items(), key=operator.itemgetter(1), reverse=True)
        for release_date in movies_release_date:
            release_date_list.insert(END, str(release_date[0] + ': ' + str(release_date[1])))

    def show_popularity(self, movies_information):
        votes_number_label = Label(self.top_window, text="Votes")
        votes_number_label.grid(row = 0, column = self._column)

        votes_number_list = Listbox(self.top_window)
        votes_number_list.grid(row = 1, column = self._column)

        self._column += 1

        movies_votes_number = sorted(movies_information['Votes_number'].items(), key=operator.itemgetter(1), reverse=True)
        for vote in movies_votes_number:
            votes_number_list.insert(END, str(vote[0] + ': ' + str(vote[1])))

    def show_movie_informations(self, movies_information):
        self.top_window.deiconify()

        self.show_ratings(movies_information)
        self.show_box_office(movies_information)
        self.show_length(movies_information)  # Test
        self.show_release_date(movies_information)  # Test
        self.show_popularity(movies_information)  # Test

        self.top_window.mainloop()

    def __init__(self):
        self._x_coordinate = 900  # Near center ;d TODO: Change it to proper center.
        self._y_coordinate = 500

        self._column = 0

        self.top_window = tkinter.Tk()
        self.set_root_window()

        self.browser_options = {}
        self.set_browser_options()

        self.directory_path = ""





def main():
    # top_window = Tk()
    #
    # rating_label = Label(top_window, text="Ratings")
    # rating_label.grid(row=0, column=0)
    #
    # rating_list = Listbox(top_window)
    # rating_list.grid(row=1, column=0)
    # rating_list.insert(1, "Benzema")
    #
    # box_office_label = Label(top_window, text="Box Office")
    # box_office_label.grid(row=0, column=1)
    #
    # box_office_list = Listbox(top_window)
    # box_office_list.grid(row=1, column=1)
    # box_office_list.insert(3, "Aua")
    #
    # top_window.mainloop()
    #
    # return

    omdb.set_default('tomatoes', True)

    manager = GUI_Manager()
    directory_path = manager.get_folder_path()

    if directory_path == "":
        directory_path = os.path.dirname(os.path.realpath(__file__))
    if len(sys.argv) == 2:
        directory_path = sys.argv[1]

    raw_movies = os.listdir(directory_path)
    movie_list = clean(raw_movies)
    movies_information = get_movies_info(movie_list)

    movies_not_recognized = movies_information['Not_recognized']

    if movies_not_recognized:
        print("\nNot recognized movies: \n")
        for movie_name in movies_not_recognized:
            print (movie_name)

    if not movies_information:
        print("No movies were found\nPlease check directory or file names")

    manager.show_movie_informations(movies_information)
    input("KEY PRESS:")




if __name__ == '__main__':
    main()
    #input("\n Press any key to exit")





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




import sys
import os
import omdb  # https://pypi.python.org/pypi/omdb#downloads
import glob
import operator
import string
import re
import datetime
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


def get_movies_info(movie_list, top_window):
    ratings = {}
    box_office = {}
    release_date = {}
    length = {}
    votes_number = {}
    full_title = {}
    movies_not_recognized = []

    current_movie_indicator = Text(top_window)
    current_movie_indicator.config(width=30, height = 5)
    current_movie_indicator.grid()
    top_window.update_idletasks()

    err_cnt = 0
    for movie_name in movie_list:
        current_movie_indicator.insert(END, "Analyzing: " + movie_name)
        top_window.update_idletasks()

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

            current_movie_indicator.delete("1.0", END)
        except:
            err_cnt += 1

    movie_informations = {'Ratings': ratings, 'Box_office': box_office, 'Release_date': release_date, 'Length': length,
                           'Votes_number': votes_number, 'Full_title': full_title, 'Not_recognized': movies_not_recognized}
    current_movie_indicator.destroy()
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


def sort_date(dates):
    """ 
    :param dates: dictionary in format {str, str}. 2nd str is date, like: 22 Jun 2007
    We want to transform it to 22-06-2007, and then sort it.
    :returns: sorted list by dates. 
    """
    months_mapping = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                     'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    for movie_name in dates:
        if dates[movie_name] != 'N/A':
            month = re.search(r'([A-z]+)', dates[movie_name])
            month = month.group()
            dates[movie_name] = dates[movie_name].replace(month, months_mapping[month])
            dates[movie_name] = dates[movie_name].replace(' ', '-')
        else:
            dates[movie_name] = '1-01-1000'

    sorted_dates = sorted(dates.items(), key=lambda current_date: datetime.datetime.strptime(current_date[1],
                                                                                             '%d-%m-%Y'), reverse=True)
    return sorted_dates


class GUI_Manager:
    def set_root_window_to_center(self):
        width = self.top_window.winfo_reqwidth()
        height = self.top_window.winfo_reqheight()
        screen_width = self.top_window.winfo_screenwidth()
        screen_height = self.top_window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.top_window.geometry('+%d+%d' % (x, y))

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

        if len(movies_information['Ratings']) < self.max_elements_before_scrolling:
            rating_list.config(width=0, height=0)  # Resizes tk_listbox to fit content.
        else:
            rating_list.config(width=0)

        rating_scroolbar = Scrollbar(self.top_window, command=rating_list.yview)
        rating_list.config(yscrollcommand = rating_scroolbar.set)
        rating_scroolbar.grid(row = 1, column = self._column)
        self._column += 1

        movies_ratings = sorted(movies_information['Ratings'].items(), key=operator.itemgetter(1), reverse=True)
        for movie_rating in movies_ratings:
            rating_list.insert(END, str(movie_rating[0] + ': ' + str(movie_rating[1])))

    def show_box_office(self, movies_information):
        box_office_label = Label(self.top_window, text="Box Office")
        box_office_label.grid(row = 0, column = self._column)

        box_office_list = Listbox(self.top_window)
        box_office_list.config(width=0, height=0)
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

        if len(movies_information['Length']) < self.max_elements_before_scrolling:
            length_list.config(width=0, height=0)  # Resizes tk_listbox to fit content.
        else:
            length_list.config(width=0)

        movie_length_scroolbar = Scrollbar(self.top_window, command=length_list.yview)
        length_list.config(yscrollcommand = movie_length_scroolbar.set)
        movie_length_scroolbar.grid(row = 1, column = self._column)
        self._column += 1

        # Strip string from length, ie: 88 min  -> 88
        for movie_name, duration in movies_information['Length'].items():
            print(movie_name)
            if duration != 'N/A':
                length_purified = int(re.match(r'\d+', duration).group())
                movies_information['Length'][movie_name] = length_purified
            else:
                movies_information['Length'][movie_name] = -1

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

        if len(movies_information['Release_date']) < self.max_elements_before_scrolling:
            release_date_list.config(width=0, height=0)  # Resizes tk_listbox to fit content.
        else:
            release_date_list.config(width=0)

        release_date_scroolbar = Scrollbar(self.top_window, command=release_date_list.yview)
        release_date_list.config(yscrollcommand = release_date_scroolbar.set)
        release_date_scroolbar.grid(row = 1, column = self._column)
        self._column += 1

        movies_release_date = sort_date(movies_information['Release_date'])
        for release_date in movies_release_date:
            release_date_list.insert(END, str(release_date[0] + ': ' + str(release_date[1])))

    def show_popularity(self, movies_information):
        votes_number_label = Label(self.top_window, text="Votes")
        votes_number_label.grid(row = 0, column = self._column)

        votes_number_list = Listbox(self.top_window)
        votes_number_list.config(width=0, height=0)
        votes_number_list.grid(row = 1, column = self._column)

        self._column += 1

        # for movie in movies_information['Votes_number']:
        #     movies_information['Votes_number'][movie] = movies_information['Votes_number'][movie].replace(',', '.')
        #     movies_information['Votes_number'][movie] = float(movies_information['Votes_number'][movie])

        movies_votes_number = sorted(movies_information['Votes_number'].items(), key=operator.itemgetter(1), reverse=True)
        for vote in movies_votes_number:
            votes_number_list.insert(END, str(vote[0] + ': ' + str(vote[1])))

    def show_not_recognized_movies(self, movies_information):
        not_recognized_label = Label(self.top_window, text="Not recognized")
        not_recognized_label.grid(row = 0, column = self._column)

        not_recognized_list = Listbox(self.top_window)
        not_recognized_list.grid(row = 1, column = self._column)
        self._column += 1

        if len(movies_information['Not_recognized']) < self.max_elements_before_scrolling:
            not_recognized_list.config(width=0, height=0)  # Resizes tk_listbox to fit content.
        else:
            not_recognized_list.config(width=0)

        not_recognized_scroolbar = Scrollbar(self.top_window, command=not_recognized_list.yview)
        not_recognized_list.config(yscrollcommand = not_recognized_scroolbar.set)
        not_recognized_scroolbar.grid(row = 1, column = self._column)

        self._column += 1

        for movie_name in movies_information['Not_recognized']:
            not_recognized_list.insert(END, movie_name)

    def show_no_movies_found(self):
        error_text_widget = Text(self.top_window)
        error_text = "Found no movies in directory: " + self.directory_path
        error_text_widget.config(width = len(error_text), height = 5)
        error_text_widget.grid()
        error_text_widget.insert(INSERT, error_text)
        self.top_window.mainloop()


    def show_movie_informations(self, movies_information):
        if len(movies_information['Ratings']) > 0:
            self.show_ratings(movies_information)
            self.show_length(movies_information)
            self.show_release_date(movies_information)
            #self.show_box_office(movies_information)  # TODO: Fix N/A to be last.
            #self.show_popularity(movies_information)  # TODO: Convert string to float for proper sorting
        if len(movies_information['Not_recognized']) > 0:
            self.show_not_recognized_movies(movies_information)
        if len(movies_information['Ratings']) == 0 and len(movies_information['Not_recognized']) == 0:
            self.show_no_movies_found()

        self.top_window.mainloop()

    def __init__(self):
        self.max_elements_before_scrolling = 20
        self._column = 0

        self.top_window = tkinter.Tk()
        self.set_root_window_to_center()

        self.browser_options = {}
        self.set_browser_options()

        self.directory_path = ""


def main():
    omdb.set_default('tomatoes', True)

    manager = GUI_Manager()
    directory_path = manager.get_folder_path()

    if directory_path == "":
        directory_path = os.path.dirname(os.path.realpath(__file__))
    if len(sys.argv) == 2:
        directory_path = sys.argv[1]

    raw_movies = os.listdir(directory_path)
    movie_list = clean(raw_movies)
    movies_information = get_movies_info(movie_list, manager.top_window)

    if not movies_information:
        print("No movies were found.\nPlease check directory or file names.")

    manager.show_movie_informations(movies_information)

if __name__ == '__main__':
    main()
    input("\n Press any key to exit.")

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

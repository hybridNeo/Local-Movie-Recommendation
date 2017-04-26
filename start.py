import sys
import os
import omdb  # https://pypi.python.org/pypi/omdb#downloads
import glob
import operator
import string
import re
from tkinter.filedialog import *


reserved_audio = ['5.1', '7.1', '5 1', '7 1', 'DUAL AUDIO', 'DUAL-AUDIO']
reserved_video = ['2160p', '4K',  '1080p', '720p', '480p', '360p', 'HD', 'FULL HD', 'FULLHD']
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


def main():
    omdb.set_default('tomatoes', True)
    dirname = askdirectory()

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
        print(i[0]+ ' --------------- ' + str(i[1]))
        found = found+1
    # search = omdb.title('The Matrix')
    # print(search.imdb_rating)
    # print(search.tomato_rating)
    if(found == 0):
        print("No movies were found\nPlease check directory or file names")

if __name__ == '__main__':
    main()
    input("\n Press any key to exit")
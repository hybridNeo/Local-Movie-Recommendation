import sys
import os
import omdb  # https://pypi.python.org/pypi/omdb#downloads
import glob
import operator
import string
import re
reserved = ['EXTENDED', 'REMASTERD', 'DIRECTORS', 'UNRATED', 'AlTERNATE', '1080p', '720p', '480p', '360p', 'HD',
            'FULL HD', 'FULLHD', 'BLURAY', '5.1', 'DUAL AUDIO', 'DUAL-AUDIO', 'x264', 'WEB-DL', 'CH', 'X264', 'BrRip',
            'Rip', 'DVDRip', 'XviD', '[]']

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
    l = []
    for i in raw_list:
        cl = i
        i = i.replace('.', ' ')
        if('(' in cl):
            cl = i.split('(')
        else:
            cl = i.split('\0')
        cl = cl[0]
        for j in reserved:
            if(j in cl):
                cl = remove(j, cl)
        cl = re.sub(r'^www.\/\/.*[\r\n]*', '', cl, flags=re.MULTILINE)
        cl = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', cl, flags=re.MULTILINE)
        l.append(cl)
    return l

def main():
    omdb.set_default('tomatoes', True)
    dirname = input("Enter directory(Press enter for root): \n")
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
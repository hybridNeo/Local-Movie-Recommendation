import sys
import os
import omdb
import glob
import operator
import string
import re
reserved = ['EXTENDED','REMASTERD','DIRECTORS','UNRATED','AlTERNATE','1080p','720p','480p','360p','HD','FULL HD','FULLHD','BLURAY','5.1','DUAL AUDIO','DUAL-AUDIO','x264', 'WEB-DL','CH','X264','BrRip','Rip','DVDRip','XviD','[]']


#Changelog:
#Line 07 - Added re module.
#Line 08 - reserved exponentially expanded.
#Line 27 - Added remove().
#Line 51 - Added i.replace() in order to replace dots for spaces.
#Line 54 - Added else statement with i.split('\0') in order to allow bigger flexibility in folder naming.
#Line 57 - reserved tags checking system refactored, it now uses remove().
#Line 60 - Added statement to remove any possible urls from filenames.
#Line 61 - Same as above, however for diffent url format.
#Line 67 - Added line break after input message, and input message changed in order to correspond with line 41.
#Line 68 - Added option to use root directory instead of typing one, therefore, using file current location upon null input.
#Line 75 - Added two line breaks after 'Retreiving(...)...' message.
#line 81 - Added space after hyphens.
#Line 86 - Added output in case of zero movies found.
#Line 90 - Added raw_input() after code execution, thus keeping it open without the need to run it through console or similar.

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
	dirname = raw_input("Enter directory(Press enter for root): \n")
	if(dirname == ""):
		dirname = os.path.dirname(os.path.realpath(__file__))
	if(len(sys.argv) ==  2):
		dirname = sys.argv[1]
	raw_movies = os.listdir(dirname)
	print('Cleaning.....')
	l = clean(raw_movies)
	print('Retreiving Info... \n \n')
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
	raw_input("\n Press any key to exit")
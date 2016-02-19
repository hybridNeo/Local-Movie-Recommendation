import sys
import os
import omdb
import glob
import operator
reserved = ['EXTENDED','REMASTERD','DIRECTORS','UNRATED','AlTERNATE']
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
		if('(' in cl):
			cl = i.split('(')
		cl = cl[0]
		for j in reserved:
		  	if(j in cl):
		  		cl.split(j)
		  		cl = cl[0]
		l.append(cl)
	return l

def main():
	omdb.set_default('tomatoes', True)
	dirname = raw_input("Enter directory")
	if(len(sys.argv) ==  2):
		dirname = sys.argv[1]
	raw_movies = os.listdir(dirname)
	print('Cleaning.....')
	l = clean(raw_movies)
	print('Retreiving Info...')
	info = search(l)
	sorted_x = sorted(info.items(), key=operator.itemgetter(1))
	sorted_x = sorted_x[::-1]
	for i in sorted_x:
		print(i[0]+ ' ---------------' + str(i[1]))
	# search = omdb.title('The Matrix')
	# print(search.imdb_rating)
	# print(search.tomato_rating)
if __name__ == '__main__':
	main()

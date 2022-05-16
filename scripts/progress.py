#!/usr/bin/env -S python3 -B

from config import *

file_name = scripts_path + '/progress_list.txt'


def read_progress():
	res = []
	
	f = open(file_name, 'rb')
	for s in f:
		lib, progress = str(s, 'utf8').strip().split(' ')
		res.append((lib, progress))
	
	return res

def write_progress(progress_list):
	f = open(file_name, 'wb')
	for lib, progress in progress_list:
		f.write(bytes(lib + ' ' + progress + '\n', 'utf8'))

if __name__ == '__main__':
	progress_list = []
	for lib in libs:
		progress_list.append([lib, 'start'])
	write_progress(progress_list)

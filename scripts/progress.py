#!/usr/bin/env -S python3 -B

from config import *

file_name = scripts_path + '/progress_list.txt'


def read_progress():
	res = []
	
	with open(file_name, 'rb') as f:
		for s in f:
			lib, progress = str(s, 'utf-8').strip().split(' ')
			res.append((lib, progress))
	
	return res

def write_progress(progress_list):
	with open(file_name, 'wb') as f:
		for lib, progress in progress_list:
			f.write(bytes(lib + ' ' + progress + '\n', 'utf-8'))

if __name__ == '__main__':
	progress_list = [(lib, 'start') for lib in libs]
	write_progress(progress_list)

#!/usr/bin/env -S python3 -B

import os

from config import *
from progress import *

conf_cmd = './conf.sh 1>conf_out.txt 2>conf_err.txt'
make_cmd = './make.sh 1>make_out.txt 2>make_err.txt'


progress_list = read_progress()
for i, (lib, progress) in enumerate(progress_list):
	if progress == 'maked': # start | configurated | maked
		continue
	
	print('Build <%s>' % lib)
	
	lib_path = sources_path + lib + '/'
	if not os.path.exists(lib_path):
		print('  Source dir not found')
		os.sys.exit(1)
	
	os.chdir(lib_path)
	
	if progress == 'start':
		print(conf_cmd)
		if os.system(conf_cmd):
			print('Error on ./conf.sh of <%s>' % lib)
			os.sys.exit(1)
		
		progress_list[i] = (lib, 'configurated')
		write_progress(progress_list)
	
	print(make_cmd)
	if os.system(make_cmd):
		print('Error on ./make.sh of <%s>' % lib)
		os.sys.exit(1)
	
	progress_list[i] = (lib, 'maked')
	write_progress(progress_list)
	
	os.chdir(sources_path)

print('Ok!')

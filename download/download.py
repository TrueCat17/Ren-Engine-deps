#!/usr/bin/env -S python3 -B

from config import *
from progress import *

import os
import shutil


def read_links():
	res = {}
	if not os.path.exists(scripts_path + 'links.txt'):
		print('File <links.txt> not found')
		os.sys.exit(1)
	
	with open(scripts_path + 'links.txt', 'rb') as f:
		for s in f:
			if s and not s.startswith(b'#'):
				lib, url = str(s, 'utf-8').split(': ')
				res[lib.strip()] = url.strip()
	
	return res

urls = read_links()
links_of = set(urls.keys())
need_libs = set(libs)
if links_of != need_libs:
	no_links = need_libs.difference(links_of)
	if no_links:
		print('No links for libs: ' + ', '.join(no_links))
	extra_links = links_of.difference(need_libs)
	if extra_links:
		print('Extra links for libs: ' + ', '.join(extra_links))
	os.sys.exit(1)



os.makedirs(download_path, exist_ok = True)
os.makedirs(sources_path,  exist_ok = True)


was_error = False
downloaded = []

progress_list = read_progress()
for i, (lib, progress) in enumerate(progress_list):
	if lib not in urls:
		print('URL for <%s> is unknown' % lib) 
		continue
	if progress != 'start':
		continue

	
	if os.path.isdir(sources_path + lib):
		shutil.rmtree(sources_path + lib)
	
	url = urls[lib]
	
	try:
		print('Download <%s>' % lib)
		
		if ' ' in url: # there are params for git
			index = url.index(' ')
			only_url = url[:index]
		else:
			only_url = url
		dirname, _ = os.path.splitext(os.path.basename(only_url))
		
		if not os.path.exists(download_path + dirname):
			os.chdir(download_path)
			cmd = 'git clone -c advice.detachedHead=false --depth=1 ' + url
			if os.system(cmd):
				print('Comand <%s> failed' % cmd)
				was_error = True
				continue
			
			if lib == 'freetype':
				cmd = 'cd ./freetype/ && ./autogen.sh && cd ..'
				if os.system(cmd):
					print('Comand <%s> failed' % cmd)
					was_error = True
					continue
		else:
			print('  use cached')
		
		downloaded.append(lib)
		
		progress_list[i] = (lib, 'downloaded')
		write_progress(progress_list)
		
	except BaseException as e:
		if type(e) is KeyboardInterrupt:
			os.sys.exit(1)
		
		was_error = True
		print('Error on download <%s>' % lib)
		print('You can repeat later or find and download by yourself')
		print(e)


if downloaded:
	print('Downloaded libs: ' + ', '.join(downloaded))
elif not was_error:
	print('Nothing to do')
